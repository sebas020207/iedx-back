from django.urls import path
from . import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/quotes', views.QuotesView.as_view()),
    path('admin/quote/<int:pk>', views.QuoteView.as_view()),
    path('quote', views.PostQuoteView.as_view()),
    path('registry', views.RegistryQuoteView.as_view()),
]
