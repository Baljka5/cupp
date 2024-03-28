from django.core.paginator import Paginator
from django.db.models import Q

from .forms import StrRentForm
from django.views import generic as g
from .models import StrRent
from django.shortcuts import render, redirect
from django.contrib import messages
from cupp.point.models import Point
from cupp.store_trainer.models import StoreTrainer


def rent_addnew(request):
    store_id_to_name = {rent.store_id: rent.store_name for rent in StoreTrainer.objects.all()}
    if request.method == "POST":
        form = StrRentForm(request.POST)
        if form.is_valid():
            try:
                form.instance.created_by = request.user if not form.instance.pk else form.instance.created_by
                form.instance.modified_by = request.user
                form.save()
                messages.success(request, "Event added successfully!")
                return redirect('/rent-index')
            except Exception as e:
                messages.error(request, f"Error saving event: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StrRentForm()
    return render(request, 'rent/index.html', {'form': form, 'store_id_to_name': store_id_to_name})


# def event_addnew(request):
#     # model = MainTable
#     # form_class = MainTableForm
#     # template_name = 'license/show.html'
#     # success_url = reverse_lazy('map')
#     if request.method == "POST":
#         form = StoreDailyLogForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('/')
#             except:
#                 pass
#     else:
#         form = StoreDailyLogForm()
#     return render(request, 'event/event_index.html', {'form': form})


def index(request):
    # Retrieve filter values from GET request
    store_id_query = request.GET.get('store_id', '')
    str_name_query = request.GET.get('str_name', '')

    # Build the query based on presence of filter values
    query = Q()
    if store_id_query:
        query &= Q(store_id__icontains=store_id_query)
    if str_name_query:
        query &= Q(id__str_name__icontains=str_name_query)

    models = StrRent.objects.filter(query).distinct().order_by('id')

    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "rent/show.html", {
        'page_obj': page_obj,
        'store_id_query': store_id_query,
        'str_name_query': str_name_query
    })


# def index(request):
#     models = StoreDailyLog.objects.all()
#     return render(request, "event/show.html", {'models': models})


def edit(request, id):
    model = StrRent.objects.get(id=id)
    return render(request, 'rent/edit.html', {'model': model})


def update(request, id):
    model = StrRent.objects.get(id=id)
    form = StrRentForm(request.POST, instance=model)
    if form.is_valid():
        form.instance.modified_by = request.user
        form.save()
        return redirect("/rent-index")
    return render(request, 'rent/edit.html', {'model': model})


def destroy(request, id):
    model = StrRent.objects.get(id=id)
    model.delete()
    return redirect("/rent-index")


class RentView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the is_event_member variable
        context['is_event_member'] = self.request.user.groups.filter(name='Rent').exists()
        return context
