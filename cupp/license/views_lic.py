from .forms import MainTableForm
from .models import MainTable
from django.shortcuts import render, redirect
from cupp.point.models import Point


def addnew(request):
    # model = MainTable
    # form_class = MainTableForm
    # template_name = 'license/show.html'
    # success_url = reverse_lazy('map')
    if request.method == "POST":
        form = MainTableForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/')
            except:
                pass
    else:
        form = MainTableForm()
    return render(request, 'license/test_form.html', {'form': form})


def index(request):
    models = MainTable.objects.all()
    return render(request, "license/show.html", {'models': models})


def edit(request, id):
    model = MainTable.objects.get(id=id)
    return render(request, 'license/edit.html', {'model': model})


def update(request, id):
    model = MainTable.objects.get(id=id)
    form = MainTableForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("/")
    return render(request, 'license/edit.html', {'model': model})


def destroy(request, id):
    model = MainTable.objects.get(id=id)
    model.delete()
    return redirect("/")
