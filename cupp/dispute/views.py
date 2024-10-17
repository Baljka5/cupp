from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .forms import DisputeForm
from .models import DisputeTable
from cupp.license.models import DimensionTable
from django.shortcuts import render, redirect
from django.contrib import messages
from cupp.store_trainer.models import StoreTrainer
from cupp.event.models import ActionOwner
from django.views import generic as g


def leg_add(request):
    store_id_to_name = {event.store_id: event.store_name for event in StoreTrainer.objects.all()}

    if request.method == "POST":
        form = DisputeForm(request.POST)
        if form.is_valid():
            try:
                # Set created_by and modified_by
                form.instance.created_by = request.user
                form.instance.modified_by = request.user

                # Set close_date to None if it's not provided
                if not form.cleaned_data.get('close_date'):
                    form.instance.close_date = None

                form.save()
                messages.success(request, 'Form submission successful.')
                return redirect('/leg-index')
            except Exception as e:
                messages.error(request, 'Form could not be saved. Please try again.')
                print(f"Error saving form: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = DisputeForm()

    return render(request, 'Dispute/index.html', {
        'form': form,
        'store_id_to_name': store_id_to_name,
    })


# def index(request):
#     models = MainTable.objects.all()
#     return render(request, "license/show.html", {'models': models})

def index(request):
    # Retrieve filter values from GET request
    store_id_query = request.GET.get('store_no', '')
    lic_id_nm_query = request.GET.get('disp_cat', '')

    # Build the query based on presence of filter values
    query = Q()
    if store_id_query:
        query &= Q(store_no__icontains=store_id_query)
    if lic_id_nm_query:
        query &= Q(disp_cat__icontains=lic_id_nm_query)

    models = DisputeTable.objects.filter(query).distinct().order_by('id')

    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "Dispute/show.html", {
        'page_obj': page_obj,
        'store_id_query': store_id_query,
        'lic_id_nm_query': lic_id_nm_query
    })


def edit(request, id):
    model = DisputeTable.objects.get(id=id)
    types = StoreTrainer.objects.all()
    owners = ActionOwner.objects.all()
    store_id_to_name = {event.store_id: event.store_name for event in StoreTrainer.objects.all()}
    return render(request, 'Dispute/edit.html',
                  {'model': model, 'types': types, 'store_id_to_name': store_id_to_name, 'owners': owners})


def update(request, id):
    model = DisputeTable.objects.get(id=id)
    types = DimensionTable.objects.all()
    owners = ActionOwner.objects.all()
    form = DisputeForm(request.POST, instance=model)

    if form.is_valid():
        # Only set close_date to None if the field is explicitly cleared by the user (i.e., empty string)
        if form.cleaned_data.get('close_date') == '':
            form.instance.close_date = None

        form.save()
        messages.success(request, 'Record updated successfully.')
        return redirect("/leg-index")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Error in {field}: {error}")

    return render(request, 'Dispute/edit.html', {'model': model, 'types': types, 'owners': owners})


#
# def update(request, id):
#     model = MainTable.objects.get(id=id)
#     types = DimensionTable.objects.all()
#     form = MainTableForm(request.POST, instance=model)
#     if form.is_valid():
#         form.save()
#         return redirect("/register-license")
#     return render(request, 'license/edit.html', {'model': model, 'types': types})
#
#
def destroy(request, id):
    model = DisputeTable.objects.get(id=id)
    model.delete()
    return redirect("/leg-index")
#
#
# class LicenseView(g.TemplateView):
#     template_name = 'base.html'
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         # Add in the is_event_member variable
#         context['is_event_member'] = self.request.user.groups.filter(name='license').exists()
#         return context
