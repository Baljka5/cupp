import json

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from cupp.store_consultant.models import Area, Consultants, Allocation, StoreConsultant
from cupp.point.models import Point
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


def scIndex(request):
    areas = Area.objects.all()
    consultants = Consultants.objects.all()
    store_consultants = StoreConsultant.objects.all()
    return render(request, 'store_consultant/index.html', {'areas': areas, 'consultants': consultants, 'store_consultants': store_consultants})


@csrf_protect
@require_POST
def update_consultant_area(request):
    consultant_id = request.POST.get('consultantId')
    target_area_id = request.POST.get('targetAreaId')

    try:
        consultant = Consultants.objects.get(id=consultant_id)

        if target_area_id == 'not-allocated':
            # Assuming that a null foreign key on consultant represents not-allocated
            consultant.area = None
        else:
            # Assuming that the area_id is a ForeignKey in Consultants model
            consultant.area = Area.objects.get(id=target_area_id)

        consultant.save()
        return JsonResponse({'status': 'success'})
    except (Consultants.DoesNotExist, Area.DoesNotExist) as e:
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)


@require_POST
def save_allocations(request):
    print(request.body)
    try:
        data = json.loads(request.body)
        allocations = data.get('allocations', [])

        with transaction.atomic():
            # Process each allocation
            for allocation in allocations:
                consultant_id = allocation.get('consultantId')
                area_id = allocation.get('areaId') if allocation.get('areaId') != 'not-allocated' else None

                # Assuming consultant_id and area_id are enough to uniquely identify an allocation,
                # adjust according to your model fields and logic.
                # Ensure you are referencing the correct foreign key fields in your update_or_create call.
                obj, created = Allocation.objects.update_or_create(
                    consultant_id=consultant_id,  # Make sure this matches your model's field name
                    defaults={'area_id': area_id}  # And this as well
                )

                obj.save()

            return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)


def get_allocations(request):
    allocations = Allocation.objects.all().values('id', 'consultant__id', 'area__id', 'year', 'month')
    return JsonResponse(list(allocations), safe=False)
