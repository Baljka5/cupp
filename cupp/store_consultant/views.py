from django.http import JsonResponse
from django.shortcuts import render
from cupp.store_consultant.models import Area, Consultants
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_consultant_area(request):
    if request.method == 'POST':
        consultant_id = request.POST.get('consultantId')
        target_area_id = request.POST.get('targetAreaId')
        # Update the consultant's area here
        # ...

        return JsonResponse({'success': 'Consultant updated successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def scIndex(request):
    areas = Area.objects.all()
    consultants = Consultants.objects.all()
    return render(request, 'store_consultant/index.html', {'areas': areas, 'consultants': consultants})
