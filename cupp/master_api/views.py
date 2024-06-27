from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cupp.store_consultant.models import StoreConsultant
from cupp.store_trainer.models import StoreTrainer
from cupp.point.models import Point, StorePlanning
from cupp.master_api.serializers import CompositeStoreSerializer

from django.shortcuts import render
from django.http import HttpResponseNotFound


def my_custom_page_not_found_view(request, exception=None):
    context = {}
    return render(request, '404.html', context, status=404)


class StoreMasterAPI(APIView):
    def get(self, request, *args, **kwargs):
        branch_no = request.query_params.get('branchNo', None)

        store_consultants = StoreConsultant.objects.filter(
            store_id=branch_no) if branch_no else StoreConsultant.objects.all()
        data = []

        if not store_consultants.exists() and branch_no:
            # If no consultants found for a specific branchNo, return a custom message
            return Response({'message': 'Store not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        for store_consultant in store_consultants:
            try:
                store_planning = StorePlanning.objects.get(store_id=store_consultant.store_id)
                store_trainer = StoreTrainer.objects.get(store_id=store_consultant.store_id)
            except (StorePlanning.DoesNotExist, StoreTrainer.DoesNotExist):
                continue

            is_24h_open = store_consultant.tt_type == "24H" if store_consultant else False

            employees_data = [{
                'position': "Дэлгүүрийн менежер",
                'name': store_consultant.sm_name if store_consultant else "N/A",
                'phone': store_consultant.sm_phone if store_consultant else "",
            }]

            data.append({
                'branchType': 'Direct',
                'branchNo': store_consultant.store_id,
                'branchAddress': store_planning.address_simple if store_trainer else None,
                'branchName': store_consultant.store_name,
                'branchOpeningDate': store_trainer.open_date if store_trainer else None,
                'branchInChargeName': store_consultant.sc_name,
                'branchInChargePhone': '',
                'areaManagerName': store_consultant.team_mgr,
                'areaManagerPhone': '',
                'branchEmployees': employees_data,
                'openTime': store_consultant.wday_hours,
                'closeTime': store_consultant.wend_hours,
                'roZone': store_planning.cluster if store_planning else '',
                'is24Open': is_24h_open,
                'closeDate': store_consultant.close_date,
                'closedDescription': store_consultant.close_reason,
            })
        if not data:
            # Return a custom message if no data was added to the list
            return Response({'message': 'Store not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompositeStoreSerializer(data, many=True)
        return Response(serializer.data)

# Ensure to import status from rest_framework
