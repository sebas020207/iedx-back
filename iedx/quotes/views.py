from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.http import Http404
from datetime import datetime
from django.db.models import Q

from .models import Quote, Registry
from .serializers import QuoteSerializer, CreateQuoteSerializer, RegistrySerializer
from iedx.settings import EMAIL_HOST_USER
# Create your views here.


class QuotesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        query_params = request.query_params
        filters = {}
        if 'date' in query_params:
            filters['date__date'] = datetime.strptime(
                query_params['date'], "%Y-%m-%dT%H:%M:%S.%f%z").date()
        if 'priority' in query_params:
            filters['priority'] = query_params['priority']
        if 'search_item' in query_params:
            filters['first_name__contains'] = query_params['search_item']

        quotes = Quote.objects.filter(**filters).order_by("-date")
        quotes = [i for n, i in enumerate(quotes) if i not in quotes[n + 1:]]

        for quote in quotes:
            quote.date = quote.date.date().strftime("%d/%m/%y")

        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)


class QuoteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        quote = self.get_object(pk)

        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

# Para PostQuoteView
# {
#     "first_name": "Latest quote",
#     "last_name": "Last name quote",
#     "email": "tstmail@gmail.com",
#     "address": "321 test address",
#     "mobile_phone": "123456789",
#     "phone": "123456789",
#     "company": "Test Co",
#     "area": "Vidrios",
#     "priority": "H",
#     "product":
#     [
#         {"id": 1},
#         {"id": 2},
#         {"id": 3}
#     ]
# }


class PostQuoteView(APIView):
    def post(self, request, format=None):
        serializer = CreateQuoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        quote_id = serializer.data['id']
        quote = Quote.objects.get(id=quote_id)
        message = quote.email_message()
        send_mail(
            'Cotización',
            message,
            EMAIL_HOST_USER,
            ['sebastianmendez281@gmail.com'],
            fail_silently=True,
        )
        return Response(serializer.data)


class RegistryQuoteView(APIView):
    def post(self, request, format=None):
        serializer = RegistrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        registry_id = serializer.data['id']
        registry = Registry.objects.get(id=registry_id)
        message = registry.email_message_registry()
        send_mail(
            'Cotización',
            message,
            EMAIL_HOST_USER,
            ['sebastianmendez281@gmail.com'],
            fail_silently=True,
        )
        return Response(serializer.data)
