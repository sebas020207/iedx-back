from rest_framework import serializers

from .models import History
from datetime import datetime


class HistorySerializer(serializers.ModelSerializer):
    hour = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ['id', 'name', 'date', 'hour', 'action']

    def get_hour(self, obj):
        return obj.date_created.time().strftime("%H:%M:%S")

    def get_date(self, obj):
        return obj.date_created.date().strftime("%d/%m/%y")
