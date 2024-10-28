import csv
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from datetime import datetime

# Database configuration
DB_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'cu_ep',
    'USER': 'readonly_user',
    'PASSWORD': 'OFNMf6Y47z6u',
    'HOST': '10.10.90.95',
    'PORT': '5432',
}


# Helper function to extract question names, scores, and other fields from nested JSON
def extract_questions_data(nested_json):
    questions_data = []
    if isinstance(nested_json, dict):
        for key, value in nested_json.items():
            if key == "questions" and isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and 'name' in item and 'question' in item:
                        questions_data.append({
                            'Category': item.get('category', ''),  # Extract "category" field
                            'Name': item.get('name', ''),  # Extract "name" field
                            'Question': item['question'],  # Extract "question" field
                            'maxScore': parse_score(item.get('maxScore', 0))  # Ensure score is properly cast
                        })
            elif isinstance(value, dict):
                questions_data.extend(extract_questions_data(value))  # Recursively check nested dictionaries
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        questions_data.extend(extract_questions_data(item))  # Recursively check list items
    return questions_data


# Helper function to convert score to an integer, defaulting to 0
def parse_score(score):
    try:
        return int(score)  # Try casting to int
    except (ValueError, TypeError):
        return 0  # Return 0 if it's not a valid number


# Main view to fetch and export data for Power BI
def fetch_powerbi_data(request):
    export_type = request.GET.get('export', None)
    start_date = request.GET.get('start_date')  # Get start date from request parameters
    end_date = request.GET.get('end_date')  # Get end date from request parameters

    # Validate the date inputs
    if not start_date or not end_date:
        return JsonResponse({'error': 'Please provide both start_date and end_date in the request parameters.'},
                            status=400)

    try:
        # Ensure the dates are in the correct format
        start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")
        # Format the dates as strings in the format PostgreSQL expects
        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S")
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Please use the correct format: YYYY-MM-DDTHH:MM.'},
                            status=400)

    # SQL query to fetch data with date filtering
    query = f"""
        SELECT
          jsonb_build_object(
            'inspection_summary',
            "inspection_summary"."Document" || jsonb_build_object('id', "inspection_summary"."Id") || jsonb_build_object(
              'CreationTime', "inspection_summary"."CreationTime"
            ) || jsonb_build_object(
              'CreatorUserId', "inspection_summary"."CreatorUserId"
            ) || jsonb_build_object(
              'LastModifierUserId', "inspection_summary"."LastModifierUserId"
            ) || jsonb_build_object(
              'LastModificationTime', "inspection_summary"."LastModificationTime"
            ),
            'inspect_plan',
            "inspect_plan"."Document" || jsonb_build_object(
              'id', "inspect_plan"."Id", 'creationTime',
              "inspect_plan"."CreationTime"
            ),
            'branch_info',
            "branch_info"."Document" || jsonb_build_object(
              'id', "branch_info"."Id", 'creationTime',
              "branch_info"."CreationTime"
            ),
            'user',
            jsonb_build_object(
              'id', "user"."Id", 'tenantId', "user"."TenantId",
              'userName', "user"."UserName", 'name',
              "user"."Name", 'surname', "user"."Surname",
              'emailAddress', "user"."EmailAddress",
              'profilePictureId', "user"."ProfilePictureId",
              'phoneNumber', "user"."PhoneNumber"
            )
          ) AS "Document"
        FROM
          "DynamicEntity" AS "inspection_summary"
          INNER JOIN "DynamicEntity" AS "inspect_plan" ON (
            "inspection_summary"."Document" ->> 'inspect_plan_id'
          ):: bigint = "inspect_plan"."Id"
          AND "inspect_plan"."DynamicEntityDefinitionId" = 8
          AND "inspection_summary"."DynamicEntityDefinitionId" = 35
          AND "inspect_plan"."IsDeleted" = false
          INNER JOIN "DynamicEntity" AS "branch_info" ON (
            "inspection_summary"."Document" ->> 'branch_id'
          ):: bigint = "branch_info"."Id"
          AND "branch_info"."DynamicEntityDefinitionId" = 23
          AND "inspection_summary"."DynamicEntityDefinitionId" = 35
          AND "branch_info"."IsDeleted" = false
          INNER JOIN "BpmUsers" AS "user" ON (
            "inspection_summary"."CreatorUserId"
          ):: bigint = ("user"."Id"):: bigint
          AND "inspection_summary"."DynamicEntityDefinitionId" = 35
          AND "user"."IsDeleted" = false
          AND "user"."TenantId" = 1
        WHERE
          (
            (
              "inspection_summary"."TenantId" = 1
              OR "inspection_summary"."IsCommon" = true
            )
          )
          AND "inspection_summary"."IsDeleted" = false
          AND "inspection_summary"."DynamicEntityDefinitionId" = 35
          AND (
            (
              "inspect_plan"."CreationTime" BETWEEN '{start_date}'
              AND '{end_date}'
              AND (
                "inspect_plan"."Document" ->> 'itemCategory_id'
              ):: numeric = 1
            )
          )
        ORDER BY
          "inspection_summary"."CreationTime" DESC
        """

    # Setting up the database connection
    connections.databases['cu_ep'] = DB_SETTINGS

    try:
        with connections['cu_ep'].cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Process the data (as before)
        # Extract question data for each document and calculate total scores
        data_for_export = {}
        unique_questions = set()
        branch_columns = set()

        for row in rows:
            document = row[0]
            questions_data = extract_questions_data(document)
            branch_no = document.get('branch_info', {}).get('branchNo', '')
            branch_columns.add(branch_no)

            for question in questions_data:
                unique_key = question['Question']

                if unique_key not in unique_questions:
                    unique_questions.add(unique_key)
                    data_for_export[unique_key] = {
                        'Name': question['Name'],
                        'Category': question['Category'],
                        'Question': question['Question'],
                    }
                data_for_export[unique_key][branch_no] = question['maxScore']

        export_data = []
        for question, details in data_for_export.items():
            for branch in branch_columns:
                if branch not in details:
                    details[branch] = 0
            export_data.append(details)

        branch_columns_list = list(branch_columns)
        headers = ['Name', 'Category', 'Question'] + branch_columns_list

        if export_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            writer = csv.DictWriter(response, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data)
            return response

        elif export_type == 'excel':
            df = pd.DataFrame(export_data)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif export_type == 'powerBI':
            # Return the data as a JSON response for Power BI
            return JsonResponse(export_data, safe=False)

        else:
            return JsonResponse(export_data, safe=False)

    except OperationalError:
        return JsonResponse({'error': 'Database connection failed'}, status=500)
