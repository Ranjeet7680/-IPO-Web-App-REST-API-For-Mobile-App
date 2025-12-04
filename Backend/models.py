# ipo_api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='public')  # 'admin' or 'public'
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'  # or email if you prefer

class Company(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class IPO(models.Model):
    STATUS_CHOICES = [
        ('upcoming','Upcoming'),
        ('open','Open'),
        ('closed','Closed'),
        ('listed','Listed'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='ipos')
    title = models.CharField(max_length=255)
    issue_start_date = models.DateField(null=True, blank=True)
    issue_end_date = models.DateField(null=True, blank=True)
    listing_date = models.DateField(null=True, blank=True)
    price_band_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_band_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    lot_size = models.IntegerField(default=1)
    total_shares = models.BigIntegerField(null=True, blank=True)
    exchange = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    short_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.company.name})"

class Document(models.Model):
    ipo = models.ForeignKey(IPO, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    title = models.CharField(max_length=255)
    file_url = models.URLField()
    is_public = models.BooleanField(default=True)
    doc_type = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
