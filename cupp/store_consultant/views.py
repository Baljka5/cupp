import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from cupp.store_consultant.models import Area, Consultants, Allocation, StoreConsultant, Tag, SC_Store_Allocation
from cupp.store_trainer.models import StoreTrainer
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from cupp.store_consultant.forms import StoreConsultantForm
from django.views import generic as g


def index(request):
    store_id_query = request.GET.get('store_id', '')
    lic_id_nm_query = request.GET.get('lic_id_nm', '')

    query = Q()
    if store_id_query:
        query &= Q(store_id__icontains=store_id_query)
    if lic_id_nm_query:
        query &= Q(lic_id__lic_id_nm__icontains=lic_id_nm_query)

    if request.user.groups.filter(name='SC Director').exists() or request.user.is_superuser:
        models = StoreConsultant.objects.all().order_by('id')
    else:
        models = StoreConsultant.objects.filter(query).distinct().order_by('id')

    # Filtering for users in the "Store Consultant" group
    if request.user.groups.filter(name='Store Consultant').exists():
        models = models.filter(sc_name__icontains=request.user.username)

    # Additional filtering for users in the "Area" group
    if request.user.groups.filter(name='Area').exists():
        models = models.filter(team_mgr__icontains=request.user.username)

    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    team_mgr = "User"
    if request.user.is_authenticated:
        consultant = StoreConsultant.objects.filter(sc_name__icontains=request.user.username).first()
        if consultant:
            team_mgr = consultant.team_mgr if consultant.team_mgr else team_mgr

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
    # Assuming team_id is passed correctly and you have a model Consultants with a related field allocation
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
def update_consultant_store(request):
    consultant_id = request.POST.get('consultantId')
    target_area_id = request.POST.get('targetAreaId')

    try:
        consultant = Consultants.objects.get(id=consultant_id)

        if target_area_id == 'not-allocated':
            consultant.area = None
        else:
            consultant.area = Area.objects.get(id=target_area_id)
        consultant.save()
        return JsonResponse({'status': 'success'})
    except (Consultants.DoesNotExist, Area.DoesNotExist) as e:
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)


@csrf_protect
@require_POST
def save_allocations(request):
    try:
        data = json.loads(request.body)
        allocations = data.get('allocations', [])

        # Debugging: Log the incoming allocations data
        print("Received allocations:", allocations)

        with transaction.atomic():
            for allocation in allocations:
                consultant_id = allocation.get('consultantId')
                area_id = allocation.get('areaId') if allocation.get('areaId') != 'not-allocated' else None
                tags = allocation.get('tags', [])

                # Fetch the consultant and create/update their allocation
                consultant = Consultants.objects.get(id=consultant_id)

                obj, created = Allocation.objects.update_or_create(
                    consultant=consultant,
                    defaults={'area_id': area_id}
                )

                if tags:
                    tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags]
                    obj.tags.set(tag_objects)

                obj.save()

        return JsonResponse({'status': 'success'})
    except Exception as e:
        # Log the full error details for easier debugging
        print(f"Error during save_allocations: {str(e)}")
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)


@csrf_protect
@require_POST
def save_consultant_stores(request):
    try:
        data = json.loads(request.body)
        print('Received store allocations:', data)  # For debugging

        store_allocations = data.get('storeAllocations', [])
        results = []

        with transaction.atomic():
            for store_allocation in store_allocations:
                consultant_id = store_allocation.get('consultantId')  # Fetch consultantId
                store_nos = store_allocation.get('storeIds', [])  # Fetch store IDs (store_no)

                # Fetch the consultant object based on consultantId
                consultant = Consultants.objects.get(id=consultant_id)
                sc_name = consultant.sc_name  # Get the sc_name for storing in the allocation

                # Clear previous allocations for this consultant
                SC_Store_Allocation.objects.filter(consultant=consultant).delete()

                # Create new allocations for the selected stores
                for store_no in store_nos:
                    # Fetch the store based on store_id
                    store = StoreConsultant.objects.get(store_id=store_no)

                    # Create a new SC_Store_Allocation object, store the consultant's sc_name and store_id
                    SC_Store_Allocation.objects.create(
                        consultant=consultant,
                        store=store,
                        store_name=store.store_name,  # Store the name of the store
                        sc_name=sc_name,  # Store the sc_name of the consultant
                        store_no=store.store_id  # Store the store_id in store_no
                    )

                results.append({
                    'status': 'success',
                    'consultant_id': consultant_id,  # Include the consultant's ID in the response
                    'sc_name': sc_name,  # Include the consultant's name in the response
                    'store_ids': store_nos  # Include the store IDs
                })

        return JsonResponse({'results': results})
    except StoreConsultant.DoesNotExist:
        print(f"Store with store_id {store_no} does not exist")
        return JsonResponse({'status': 'failed', 'message': f'Store with store_id {store_no} does not exist'},
                            status=400)
    except Consultants.DoesNotExist:
        print(f"Consultant with id {consultant_id} does not exist")
        return JsonResponse({'status': 'failed', 'message': f'Consultant with id {consultant_id} does not exist'},
                            status=400)
    except Exception as e:
        # Log the full error details for easier debugging
        print(f"Error saving consultant stores: {str(e)}")
        return JsonResponse({'status': 'failed', 'message': str(e)}, status=500)


def get_allocations(request):
    allocations = Allocation.objects.all().values('id', 'consultant__id', 'area__id', 'year', 'month')
    return JsonResponse(list(allocations), safe=False)


class StoreConsultantView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the is_event_member variable
        context['is_event_member'] = self.request.user.groups.filter(name='Store Consultant').exists()
        return context


class AreaView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['is_event_member'] = self.request.user.groups.filter(name='Area').exists()
        return context


class SCDirectorView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['is_event_member'] = self.request.user.groups.filter(name='SC Director').exists()
        return context


def get_scs_by_team(request, team_id):
    scs = Consultants.objects.filter(allocation__area_id=team_id)
    sc_data = []

    for sc in scs:
        # Get the store IDs and names allocated to the consultant
        store_allocations = SC_Store_Allocation.objects.filter(consultant=sc)
        store_ids = list(store_allocations.values_list('store__store_id', flat=True))  # Get store IDs
        store_names = list(store_allocations.values_list('store_name', flat=True))  # Get store names

        sc_data.append({
            "id": sc.id,
            "name": sc.sc_name,
            "store_ids": store_ids,  # Send store IDs to frontend
            "store_names": store_names  # Send store names to frontend
        })

    return JsonResponse({'scs': sc_data})


def assign_stores(request):
    if request.method == 'POST':
        store_ids = request.POST.getlist('store_ids')
        consultant_id = request.POST.get('consultant_id')
        consultant = Consultants.objects.get(id=consultant_id)

        # Clear previous stores assignments
        consultant.stores.clear()

        # Add new stores based on selected options
        consultant.stores.add(*store_ids)
        return redirect('some-view-name')
    else:
        stores = StoreConsultant.objects.all()
        return render(request, 'assign_stores.html', {'stores': stores})
# def get_unallocated_stores(request):
#     unallocated_stores = StoreConsultant.objects.filter(allocation__isnull=True)
#     store_data = [{'store_id': store.store_id} for store in unallocated_stores]
#     return JsonResponse({'stores': store_data})
