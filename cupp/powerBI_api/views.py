import csv
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.db import connections
from django.db.utils import OperationalError

DB_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'cu_ep',
    'USER': 'readonly_user',
    'PASSWORD': 'OFNMf6Y47z6u',
    'HOST': '10.10.90.95',
    'PORT': '5432',
}


# Helper function to extract question names, scores, and other fields
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
                            'Score': parse_score(item.get('score', 0))  # Ensure score is properly cast
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


def fetch_powerbi_data(request):
    export_type = request.GET.get('export', None)

    # Updated query based on the one you provided
    query = """
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
          "inspect_plan"."CreationTime" BETWEEN '2024-10-15T16:00:00.000Z'
          AND '2024-10-18T15:59:59.999Z'
          AND (
            "inspect_plan"."Document" ->> 'itemCategory_id'
          ):: numeric = 1  -- 83550-office, 1-delguur,788-niiluulegch,2005-aguulah
        )
      )
    ORDER BY
      "inspection_summary"."CreationTime" DESC
    """

    connections.databases['cu_ep'] = {
        'ENGINE': DB_SETTINGS['ENGINE'],
        'NAME': DB_SETTINGS['NAME'],
        'USER': DB_SETTINGS['USER'],
        'PASSWORD': DB_SETTINGS['PASSWORD'],
        'HOST': DB_SETTINGS['HOST'],
        'PORT': DB_SETTINGS['PORT'],
    }

    try:
        with connections['cu_ep'].cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Extract question data for each document and calculate total scores
        data_for_excel = {}
        unique_questions = set()  # Track unique questions
        branch_columns = set()  # Track unique branch columns

        for row in rows:
            document = row[0]
            questions_data = extract_questions_data(document)
            branch_no = document.get('branch_info', {}).get('branchNo', '')  # Extract branchNo
            branch_columns.add(branch_no)  # Add unique branch numbers to be used as columns

            for question in questions_data:
                unique_key = question['Question']

                # Ensure there are no duplicate questions
                if unique_key not in unique_questions:
                    unique_questions.add(unique_key)
                    # Initialize the row with the question details
                    data_for_excel[unique_key] = {
                        'Name': question['Name'],  # Add the Name column
                        'Category': question['Category'],  # Add the Category column
                        'Question': question['Question'],
                    }
                # Add the score under the respective branchNo
                data_for_excel[unique_key][branch_no] = question['Score']

        # Prepare the data for export
        export_data = []
        for question, details in data_for_excel.items():
            # Ensure all branch columns are present
            for branch in branch_columns:
                if branch not in details:
                    details[branch] = 0  # Default score is 0 if not present
            export_data.append(details)

        # Handle export requests for CSV or Excel
        branch_columns_list = list(branch_columns)
        headers = ['Name', 'Category', 'Question'] + branch_columns_list  # Dynamic headers based on branch numbers

        if export_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

            writer = csv.DictWriter(response, fieldnames=headers)
            writer.writeheader()
            writer.writerows(export_data)  # Write the data to CSV

            return response

        elif export_type == 'excel':
            df = pd.DataFrame(export_data)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            df.to_excel(response, index=False)
            return response

        # Default response: JSON format
        return JsonResponse(export_data, safe=False)

    except OperationalError:
        return JsonResponse({'error': 'Database connection failed'}, status=500)
