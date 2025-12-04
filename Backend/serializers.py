# ipo_api/serializers.py
from rest_framework import serializers
from .models import Company, IPO, Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','title','file_url','is_public','doc_type','created_at']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','name','ticker','description','sector','website','created_at']

class IPOSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = IPO
        fields = ['id','company','title','issue_start_date','issue_end_date','listing_date',
                  'price_band_min','price_band_max','lot_size','total_shares','exchange','status','short_description','documents']
