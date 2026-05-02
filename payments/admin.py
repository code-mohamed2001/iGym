from django.contrib import admin

from .models import Invoice

# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'customer',
                    'subscription', 'amount', 'status', 'payment_type', 'created_by']
    search_fields = ['id', 'created_at', 'customer__full_name',
                     'subscription__kind', 'amount', 'status', 'payment_type', 'created_by__first_name']
    list_filter = ['id', 'created_at',
                   'subscription',  'status', 'payment_type', 'created_by']
