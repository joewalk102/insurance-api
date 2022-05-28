from rest_framework import routers
from quote import views


quote_router = routers.DefaultRouter()


quote_router.register(r"quotes", views.QuoteViewSet, basename="quote")
quote_router.register(r"purchase", views.QuotePurchaseViewSet, basename="purchase")
