from django.http import JsonResponse
from django.core.serializers import serialize
from cupp.license.models import MainTable

def get_table_data(request):
    """
    View to return data for the main table in JSON format.
    """
    if request.is_ajax():
        # Fetch data from MainTable
        data = MainTable.objects.all()

        # Serialize the data
        serialized_data = serialize('json', data, use_natural_foreign_keys=True)

        # Return the serialized data as JSON
        return JsonResponse({'data': serialized_data}, safe=False)

    # If not AJAX request, return an empty JSON response or error
    return JsonResponse({'error': 'Invalid request'}, status=400)
