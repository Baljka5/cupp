from rest_framework.views import APIView
from rest_framework.response import Response
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
        for store_consultant in store_consultants:
            try:
                store_planning = StorePlanning.objects.get(store_id=store_consultant.store_id)
                store_trainer = StoreTrainer.objects.get(store_id=store_consultant.store_id)
            except (StorePlanning.DoesNotExist, StoreTrainer.DoesNotExist):
                continue

            # def truncate_after_second_comma(address):
            #     parts = address.split(',', 2)
            #     if len(parts) > 2:
            #         return ', '.join(parts[:2])
            #     return address
            #
            # address_detail = truncate_after_second_comma(store_planning.address_det) if store_planning and hasattr(
            #     store_planning, 'address_det') else 'Address not available'

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

        serializer = CompositeStoreSerializer(data, many=True)
        return Response(serializer.data)
