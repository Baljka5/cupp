import json

from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from cupp.store_consultant.models import Area, Consultants, Allocation, StoreConsultant
from cupp.store_trainer.models import StoreTrainer
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from cupp.store_consultant.forms import StoreConsultantForm


def index(request):
    # Retrieve filter values from GET request
    store_id_query = request.GET.get('store_id', '')
    lic_id_nm_query = request.GET.get('lic_id_nm', '')

    # Build the query based on presence of filter values
    query = Q()
    if store_id_query:
        query &= Q(store_id__icontains=store_id_query)
    if lic_id_nm_query:
        query &= Q(lic_id__lic_id_nm__icontains=lic_id_nm_query)

    models = StoreConsultant.objects.filter(query).distinct().order_by('id')

    # Filter by user if not superuser
    if not request.user.is_superuser and request.user.is_authenticated:
        models = models.filter(sc_name__icontains=request.user.username)

    # Paginator setup
    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    team_mgr = "User"
    if request.user.is_authenticated:
        consultant = StoreConsultant.objects.filter(sc_name__icontains=request.user.username).first()
        if consultant:
            team_mgr = consultant.team_mgr if consultant.team_mgr else team_mgr

    # Render the page with context
    return render(request, "store_consultant/show.html", {
        'page_obj': page_obj,
        'store_id_query': store_id_query,
        'lic_id_nm_query': lic_id_nm_query,
        'user_name': request.user.username,
        'team_mgr': team_mgr
    })


def sc_view(request, id):
    model = StoreConsultant.objects.get(id=id)
    st_model = StoreTrainer.objects.get(id=id)

    return render(request, 'store_consultant/sc_index.html', {'model': model, 'st_model': st_model})


def edit(request, id):
    model = StoreConsultant.objects.get(id=id)
    return render(request, 'store_consultant/edit.html', {'model': model})


def update(request, id):
    model = StoreConsultant.objects.get(id=id)
    form = StoreConsultantForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("/store-index")
    return render(request, 'store_consultant/edit.html', {'model': model})


def scIndex(request):
    areas = Area.objects.all()
    consultants = Consultants.objects.all()
    store_consultants = StoreConsultant.objects.all()
    return render(request, 'store_consultant/index.html',
                  {'areas': areas, 'consultants': consultants, 'store_consultants': store_consultants})


def get_team_data(request, team_id):
    # Assuming `team_id` is passed correctly and you have a model `Consultants` with a related field `allocation`
    scs = Consultants.objects.filter(allocation__area_id=team_id).values('id', 'sc_name')
    team_scs = list(scs)
    # Assuming you need to pass store allocations or other details, add them here
    return JsonResponse({'team_scs': team_scs})


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
    try:
        data = json.loads(request.body)
        print(data)
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
