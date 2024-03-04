from django.http import JsonResponse
from django.shortcuts import render
from cupp.store_consultant.models import Area, Consultants


# Create your views here.
def scIndex(request):
    areas = Area.objects.all()
    consultants = Consultants.objects.all()
    return render(request, 'store_consultant/index.html', {'areas': areas, 'consultants': consultants})
