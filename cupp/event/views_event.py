from django.core.paginator import Paginator
from django.db.models import Q

from .forms import StoreDailyLogForm
from django.views import generic as g
from .models import StoreDailyLog, ActionCategory, ActionOwner
from django.shortcuts import render, redirect
from django.contrib import messages
from cupp.point.models import Point


def event_addnew(request):
    if request.method == "POST":
        form = StoreDailyLogForm(request.POST)
        if form.is_valid():
            try:
                form.instance.created_by = request.user if not form.instance.pk else form.instance.created_by
                form.instance.modified_by = request.user
                form.save()
                messages.success(request, "Event added successfully!")
                return redirect('/log-index')
            except Exception as e:
                messages.error(request, f"Error saving event: {e}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StoreDailyLogForm()
    return render(request, 'event/event_index.html', {'form': form})


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
    store_no_query = request.GET.get('store_no', '')
    activ_cat_query = request.GET.get('activ_cat', '')  # Get the search query parameter
    query = Q()
    if store_no_query:
        query &= Q(store_no__icontains=store_no_query)
    if activ_cat_query:
        query &= Q(activ_cat__activ_cat__icontains=activ_cat_query)

    models = StoreDailyLog.objects.filter(query).distinct().order_by('id')  # And here as well

    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "event/show.html",
                  {'page_obj': page_obj, 'store_no_query': store_no_query, 'activ_cat_query': activ_cat_query})


# def index(request):
#     models = StoreDailyLog.objects.all()
#     return render(request, "event/show.html", {'models': models})


def edit(request, id):
    model = StoreDailyLog.objects.get(id=id)
    categories = ActionCategory.objects.all()
    owners = ActionOwner.objects.all()
    return render(request, 'event/edit.html', {'model': model, 'categories': categories, 'owners': owners})


def update(request, id):
    model = StoreDailyLog.objects.get(id=id)
    form = StoreDailyLogForm(request.POST, instance=model)
    if form.is_valid():
        form.instance.modified_by = request.user
        form.save()
        return redirect("/log-index")
    return render(request, 'event/edit.html', {'model': model})


def destroy(request, id):
    model = StoreDailyLog.objects.get(id=id)
    model.delete()
    return redirect("/log-index")


class EventView(g.TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the is_event_member variable
        context['is_event_member'] = self.request.user.groups.filter(name='Event').exists()
        return context
