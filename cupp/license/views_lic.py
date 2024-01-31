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


# def index(request):
#     models = MainTable.objects.all()
#     return render(request, "license/show.html", {'models': models})

def index(request):
    search_query = request.GET.get('search', '')  # Get the search query parameter
    if search_query:
        models = MainTable.objects.filter(
            # Add your search logic here, e.g., filtering by store_id
            store_id__icontains=search_query
        )
    else:
        models = MainTable.objects.all()

    paginator = Paginator(models, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "license/show.html", {'page_obj': page_obj, 'search_query': search_query})

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
