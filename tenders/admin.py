from django.contrib import admin
from .models import Tender, TenderApplication

admin.site.register([Tender, TenderApplication])