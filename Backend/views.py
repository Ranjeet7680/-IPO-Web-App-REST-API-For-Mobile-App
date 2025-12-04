# ipo_api/views.py
from rest_framework import viewsets, permissions, filters
from .models import IPO, Company, Document
from .serializers import IPOSerializer, CompanySerializer, DocumentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class IPOViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IPO.objects.select_related('company').prefetch_related('documents').all()
    serializer_class = IPOSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company__name', 'company__sector', 'exchange']
    ordering_fields = ['issue_start_date', 'listing_date', 'price_band_min']
    permission_classes = [permissions.AllowAny]

    @action(detail=False)
    def upcoming(self, request):
        qs = self.get_queryset().filter(status='upcoming').order_by('issue_start_date')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]

class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # public docs visible to anyone, but for non-public you need JWT
    def get_queryset(self):
        qs = super().get_queryset()
        # if not authenticated, only public
        user = self.request.user
        if not user or not user.is_authenticated:
            return qs.filter(is_public=True)
        return qs
