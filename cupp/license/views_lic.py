from django.core.paginator import Paginator
from django.http import JsonResponse

from .forms import MainTableForm
from .models import MainTable, DimensionTable
from django.shortcuts import render, redirect


def addnew(request):
    if request.method == "POST":
        form = MainTableForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/register-license')
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
    types = DimensionTable.objects.all()
    form = MainTableForm(request.POST, instance=model)
    if form.is_valid():
        form.save()
        return redirect("/register-license")
    return render(request, 'license/edit.html', {'model': model, 'types': types})


def destroy(request, id):
    model = MainTable.objects.get(id=id)
    model.delete()
    return redirect("/register-license")
