from django.contrib import admin

from .models import CheckIn


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['customer_barcode', 'customer__full_name',
                    'visit_type', 'created_at', 'created_by']
    list_filter = ['visit_type', 'created_by']
    search_fields = ['customer__full_name__istartwith']
    list_per_page = 50
