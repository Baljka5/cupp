from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .forms import MainTableForm, DisputeForm
from .models import MainTable, DimensionTable, DisputeTable
from cupp.point.models import District
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic as g
from django.contrib.auth.decorators import login_required
from cupp.store_trainer.models import StoreTrainer
from cupp.event.models import ActionOwner


@login_required
def addnew(request):
    lic_id_to_name = {dimension.lic_id: dimension.lic_id_nm for dimension in DimensionTable.objects.all()}
    store_id_to_name = {store.store_id: store.store_name for store in StoreTrainer.objects.all()}

    # Instantiate both forms
    form = MainTableForm(request.POST or None)
    dispute_form = DisputeForm(request.POST or None)

    if request.method == "POST":
        # Handle the submission of the MainTableForm when "Save Main Details" button is clicked
        if 'save_main' in request.POST and form.is_valid():
            store_id = form.cleaned_data.get('store_id')
            if store_id:
                try:
                    store_trainer_instance = StoreTrainer.objects.get(store_id=store_id)
                    form.instance.store_id = store_trainer_instance
                except StoreTrainer.DoesNotExist:
                    messages.error(request, f"Store ID {store_id} is invalid.")
                    return render(request, 'license/test_form.html', {
                        'form': form,
                        'dispute_form': dispute_form,
                        'lic_id_to_name': lic_id_to_name,
                        'store_id_to_name': store_id_to_name
                    })
            form.instance.created_by = request.user if not form.instance.pk else form.instance.created_by
            form.instance.modified_by = request.user
            form.save()
            messages.success(request, 'Main form submission successful.')
            return redirect('/register-license')

        # Handle the submission of the DisputeForm when "Save Dispute" button is clicked
        elif 'save_dispute' in request.POST and dispute_form.is_valid():
            store_no = dispute_form.cleaned_data.get('store_no')
            store_name = store_id_to_name.get(store_no)

            if store_name:
                # Ensure store_no and store_name are set before saving
                dispute_form.instance.store_no = store_no
                dispute_form.instance.store_name = store_name
                dispute_form.instance.created_by = request.user if not dispute_form.instance.pk else dispute_form.instance.created_by
                dispute_form.instance.modified_by = request.user
                dispute_form.save()
                messages.success(request, 'Dispute form submission successful.')
                return redirect('/register-license')
            else:
                messages.error(request, f"Invalid Store No: {store_no}")
                # Re-populate the form with the submitted values
                dispute_form = DisputeForm(request.POST)

    # Render the form with the appropriate context
    return render(request, 'license/test_form.html', {
        'form': form,
        'dispute_form': dispute_form,
        'lic_id_to_name': lic_id_to_name,
        'store_id_to_name': store_id_to_name
    })


# def index(request):
#     models = MainTable.objects.all()
#     return render(request, "license/show.html", {'models': models})

@login_required
def index(request):
    store_id_query = request.GET.get('store_id', '')
    lic_id_nm_query = request.GET.get('lic_id_nm', '')
    query = Q()
    if store_id_query:
        query &= Q(store_id__icontains=store_id_query)
    if lic_id_nm_query:
        query &= Q(lic_id__lic_id_nm__icontains=lic_id_nm_query)

    models = MainTable.objects.filter(query).distinct().order_by('id')
    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    disputes = DisputeTable.objects.all() if request.user.groups.filter(
        name='legal_team').exists() or request.user.is_superuser else None

    return render(request, "license/show.html", {
        'page_obj': page_obj,
        'store_id_query': store_id_query,
        'lic_id_nm_query': lic_id_nm_query,
        'disputes': disputes
    })


@login_required
def edit(request, id):
    model = get_object_or_404(MainTable, id=id)
    try:
        dispute_table = DisputeTable.objects.get(id=id)
    except DisputeTable.DoesNotExist:
        dispute_table = None  # Handle this scenario appropriately

    types = DimensionTable.objects.all()
    districts = District.objects.all()
    owners = ActionOwner.objects.all()  # Ensure this retrieves the correct data
    store_id_to_name = {dispute.store_id: dispute.store_name for dispute in StoreTrainer.objects.all()}

    context = {
        'model': model,
        'types': types,
        'districts': districts,
        'dispute_table': dispute_table,
        'store_id_to_name': store_id_to_name,
        'owners': owners  # Pass this to the template for use in the form
    }
    return render(request, 'license/edit.html', context)



@login_required
def update(request, id):
    model = get_object_or_404(MainTable, id=id)
    dispute_model = get_object_or_404(DisputeTable, id=id)

    form = MainTableForm(request.POST or None, instance=model)
    dispute_form = DisputeForm(request.POST or None, instance=dispute_model)

    if request.method == 'POST':
        # Check if the License update button was clicked
        if 'license_update' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'License update successful.')
                return redirect("/register-license")
            else:
                messages.error(request, 'There were errors in the license form. Please correct them.')

        # Check if the Dispute update button was clicked
        elif 'dispute_update' in request.POST:
            if dispute_form.is_valid():
                dispute_form.save()
                messages.success(request, 'Dispute update successful.')
                return redirect("/register-license")
            else:
                # Log and display errors in the dispute form
                print(dispute_form.errors)  # This will log form errors in the console
                messages.error(request, 'There were errors in the dispute form. Please correct them.')

    return render(request, 'license/edit.html', {
        'form': form,
        'dispute_form': dispute_form,
        'model': model,
        'dispute_model': dispute_model
    })


def destroy(request, id, table):
    if table == 'main':
        model = get_object_or_404(MainTable, id=id)
        model.delete()
    elif table == 'dispute':
        dispute = get_object_or_404(DisputeTable, id=id)
        dispute.delete()
    messages.success(request, 'Deletion successful')
    return redirect("/register-license")


class LicenseView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the is_event_member variable
        context['is_event_member'] = self.request.user.groups.filter(name='license').exists()
        return context


class LegalTeamView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the is_event_member variable
        context['is_event_member'] = self.request.user.groups.filter(name='legal_team').exists()
        return context
