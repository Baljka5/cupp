from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cupp.store_consultant.models import StoreConsultant
from cupp.store_trainer.models import StoreTrainer
from cupp.point.models import Point, StorePlanning
from cupp.master_api.serializers import CompositeStoreSerializer


class StoreMasterAPI(APIView):
    def get(self, request, *args, **kwargs):
        branch_no = request.query_params.get('branchNo', None)

        store_consultants = StoreConsultant.objects.filter(
            store_id=branch_no) if branch_no else StoreConsultant.objects.all()
        data = []

        if not store_consultants.exists() and branch_no:
            return Response({'message': 'Store not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        for store_consultant in store_consultants:
            store_plannings = StorePlanning.objects.filter(store_id=store_consultant.store_id)
            store_trainer = StoreTrainer.objects.filter(store_id=store_consultant.store_id).first()

            if not store_plannings.exists() or not store_trainer:
                continue

            is_24h_open = store_consultant.tt_type == "24H" if store_consultant else False

            employees_data = [{
                'position': "Дэлгүүрийн менежер",
                'name': store_consultant.sm_name if store_consultant else "N/A",
                'phone': store_consultant.sm_phone if store_consultant else "",
            }]

            for store_planning in store_plannings:
                data.append({
                    'branchType': 'Direct',
                    'branchNo': store_consultant.store_id,
                    'branchAddress': store_planning.address_simple if store_planning else None,
                    'branchName': store_consultant.store_name,
                    'branchOpeningDate': store_trainer.open_date if store_trainer else None,
                    'branchInChargeEmail': store_consultant.sc_name,
                    'branchInChargePhone': '',
                    'areaManagerEmail': store_consultant.team_mgr,
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
            return Response({'message': 'Store not found', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompositeStoreSerializer(data, many=True)
        return Response(serializer.data)
