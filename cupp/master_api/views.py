# from rest_framework.views import APIView
# from rest_framework.response import Response
# from cupp.store_consultant.models import StoreConsultant
# from cupp.store_trainer.models import StoreTrainer
# from cupp.point.models import Point, StorePlanning
# from cupp.master_api.serializers import CompositeStoreSerializer
#
#
# class StoreMasterAPI(APIView):
#     def get(self, request, *args, **kwargs):
#         store_consultant = StoreConsultant.objects.first()  # Simplified fetching logic
#         store_planning = StorePlanning.objects.first()
#         point = Point.objects.first()
#         store_trainer = StoreTrainer.objects.first()
#
#         data = {
#             'branchType': 'Direct',  # Example static data
#             'branchNo': store_consultant.store_id if store_consultant else '',
#             'branchAddress': store_planning.address_det if store_planning else '',
#             'branchName': store_consultant.store_name if store_consultant else '',
#             'branchOpeningDate': store_trainer.open_date if store_trainer else None,
#             'branchInChargeName': store_consultant.sc_name if store_consultant else '',
#             'branchInChargePhone': '123-456-7890',  # Example static data
#             'areaManagerName': store_consultant.team_mgr if store_consultant else '',
#             'openTime': store_consultant.wday_hours if store_consultant else '',
#             'closeTime': store_consultant.wend_hours if store_consultant else '',
#             'roZone': store_planning.cluster if store_planning else '',
#             'is24Open': True,  # Example static data
#             'closeDate': store_consultant.close_date if store_consultant else None,
#             'closedDescription': store_consultant.close_reason if store_consultant else ''
#         }
#
#         serializer = CompositeStoreSerializer(data)
#         return Response(serializer.data)
