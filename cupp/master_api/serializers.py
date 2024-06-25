# from rest_framework import serializers
# from cupp.store_consultant.models import StoreConsultant
# from cupp.store_trainer.models import StoreTrainer
# from cupp.point.models import Point, StorePlanning
#
#
# class StoreConsultantSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreConsultant
#         fields = ['store_id', 'store_name', 'team_mgr', 'sc_name', 'sm_num']
#
#
# class StorePlanningSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StorePlanning
#         fields = ['cluster']
#
#
# class PointSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Point
#         fields = ['address_det']
#
#
# class StoreTrainerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreTrainer
#         fields = ['open_date']
#
#
# # Composite Serializer
# class CompositeStoreSerializer(serializers.Serializer):
#     branchType = serializers.CharField()  # Manually provide data in the view
#     branchNo = serializers.CharField()
#     branchAddress = serializers.CharField()
#     branchName = serializers.CharField()
#     branchOpeningDate = serializers.DateField()
#     branchInChargeName = serializers.CharField()
#     branchInChargePhone = serializers.CharField()
#     areaManagerName = serializers.CharField()
#     openTime = serializers.CharField()
#     closeTime = serializers.CharField()
#     roZone = serializers.CharField()
#     is24Open = serializers.BooleanField()
#     closeDate = serializers.DateField()
#     closedDescription = serializers.CharField()
