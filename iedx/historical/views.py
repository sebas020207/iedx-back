from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseForbidden
from datetime import datetime

from .models import History
from .serializers import HistorySerializer
# Create your views here.


class HistoryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if not request.user.role:
            return HttpResponseForbidden("Unauthorized")

        search_item = request.query_params.items()

        filters = {
            ('date_created__date' if key == 'order_by' else 'action__contains'): (value if key != 'order_by' else datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z").date())
            for (key, value) in search_item
        }
        historical = History.objects.filter(**filters).order_by("-date_created")

        serializer = HistorySerializer(historical, many=True)
        return Response(serializer.data)
