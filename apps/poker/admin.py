from django.contrib import admin
from .models import TableSize, BuyIn, Table

admin.site.register([TableSize, BuyIn, Table])
