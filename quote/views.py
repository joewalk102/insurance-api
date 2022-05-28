from rest_framework import viewsets
from rest_framework import permissions
from quote.serializers import QuoteSerializer
from quote.models import Quote
from utils.filters import AllowStaffLimitUserFilterBackend

__all__ = ["QuoteViewSet"]


class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [AllowStaffLimitUserFilterBackend]
