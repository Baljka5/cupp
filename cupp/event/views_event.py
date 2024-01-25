from .forms import StoreDailyLogForm
from .models import StoreDailyLog, ActionCategory, ActionOwner
from django.shortcuts import render, redirect
from django.contrib import messages
from cupp.point.models import Point


def event_addnew(request):
    if request.method == "POST":
        form = StoreDailyLogForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Event added successfully!")
                return redirect('/')
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
    models = StoreDailyLog.objects.all()
    return render(request, "event/show.html", {'models': models})


def edit(request, id):
    model = StoreDailyLog.objects.get(id=id)
    categories = ActionCategory.objects.all()
    owners = ActionOwner.objects.all()
    return render(request, 'event/edit.html', {'model': model, 'categories': categories, 'owners': owners})


def update(request, id):
    model = StoreDailyLog.objects.get(id=id)
    form = StoreDailyLogForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'event/edit.html', {'model': model})


def destroy(request, id):
    model = StoreDailyLog.objects.get(id=id)
    model.delete()
    return redirect("/")
