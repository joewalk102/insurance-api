from rest_framework import viewsets
from rest_framework import permissions
from quote.serializers import QuoteSerializer
from quote.serializers import QuotePurchaseSerializer
from quote.models import Quote
from quote.models import QuotePurchase
from utils.filters import AllowStaffLimitUserFilterBackend

__all__ = ["QuoteViewSet", "QuotePurchaseViewSet"]


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [AllowStaffLimitUserFilterBackend]


class QuotePurchaseViewSet(viewsets.ModelViewSet):
    queryset = QuotePurchase.objects.all()
    serializer_class = QuotePurchaseSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [AllowStaffLimitUserFilterBackend]
