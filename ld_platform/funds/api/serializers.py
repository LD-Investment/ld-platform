from rest_framework import serializers

from ld_platform.funds.models import Fund


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ["name"]
