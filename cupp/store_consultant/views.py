from django.shortcuts import render


# Create your views here.
def scIndex(request):
    list_a = ...  # Fetch or define your list A items
    list_b = ...  # Fetch or define your list B items
    return render(request, 'store_consultant/index.html', {'list_a': list_a, 'list_b': list_b})
