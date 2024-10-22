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


# Helper function to flatten JSON
def flatten_json(nested_json, parent_key='', sep='_'):
    items = []
    for key, value in nested_json.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    # If the list item is a dict, flatten it
                    items.extend(flatten_json(item, f"{new_key}_{i}", sep=sep).items())
                else:
                    # Otherwise, treat it as a simple value
                    items.append((f"{new_key}_{i}", item))
        else:
            items.append((new_key, value))
    return dict(items)


def fetch_powerbi_data(request):
    export_type = request.GET.get('export', None)

    query = """
    SELECT
      jsonb_build_object(
        'safety_summary',
        "safety_summary"."Document" || jsonb_build_object('id', "safety_summary"."Id") || jsonb_build_object(
          'CreationTime', "safety_summary"."CreationTime"
        ) || jsonb_build_object(
          'CreatorUserId', "safety_summary"."CreatorUserId"
        ) || jsonb_build_object(
          'LastModifierUserId', "safety_summary"."LastModifierUserId"
        ) || jsonb_build_object(
          'LastModificationTime', "safety_summary"."LastModificationTime"
        ),
        'safety_inspect_plan',
        "safety_inspect_plan"."Document" || jsonb_build_object(
          'id', "safety_inspect_plan"."Id",
          'creationTime', "safety_inspect_plan"."CreationTime"
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
      "DynamicEntity" AS "safety_summary"
      INNER JOIN "DynamicEntity" AS "safety_inspect_plan" ON (
        "safety_summary"."Document" ->> 'safety_inspect_plan_id'
      ):: bigint = "safety_inspect_plan"."Id"
      AND "safety_inspect_plan"."DynamicEntityDefinitionId" = 57
      AND "safety_summary"."DynamicEntityDefinitionId" = 61
      AND "safety_inspect_plan"."IsDeleted" = false
      INNER JOIN "DynamicEntity" AS "branch_info" ON (
        "safety_summary"."Document" ->> 'branch_id'
      ):: bigint = "branch_info"."Id"
      AND "branch_info"."DynamicEntityDefinitionId" = 23
      AND "safety_summary"."DynamicEntityDefinitionId" = 61
      AND "branch_info"."IsDeleted" = false
      INNER JOIN "BpmUsers" AS "user" ON (
        "safety_summary"."CreatorUserId"
      ):: bigint = ("user"."Id"):: bigint
      AND "safety_summary"."DynamicEntityDefinitionId" = 61
      AND "user"."IsDeleted" = false
      AND "user"."TenantId" = 1
    WHERE
      (
        (
          "safety_summary"."TenantId" = 1
          OR "safety_summary"."IsCommon" = true
        )
      )
      AND "safety_summary"."IsDeleted" = false
      AND "safety_summary"."DynamicEntityDefinitionId" = 61
      AND (
        (
          "safety_inspect_plan"."CreationTime" BETWEEN '2024-10-10T16:00:00.000Z'
          AND '2024-10-18T15:59:59.999Z'
        )
      )
    ORDER BY
      "safety_summary"."CreationTime" DESC
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

        # Flatten the response data
        flattened_data = []
        for row in rows:
            document = row[0]
            flattened_data.append(flatten_json(document))

        # Handle export requests for CSV or Excel
        if export_type == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

            writer = csv.writer(response)
            writer.writerow(flattened_data[0].keys())  # Write CSV headers
            for row in flattened_data:
                writer.writerow(row.values())  # Write CSV data

            return response

        elif export_type == 'excel':
            df = pd.DataFrame(flattened_data)
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            df.to_excel(response, index=False)
            return response

        # Default response: JSON format
        return JsonResponse(flattened_data, safe=False)

    except OperationalError:
        return JsonResponse({'error': 'Database connection failed'}, status=500)
