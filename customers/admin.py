from django.contrib import admin

from .models import Customer, Subscription


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'barcode', 'phone', 'id_number']
    search_fields = ['full_name__istartswith', 'barcode', 'phone__istartswith']
    # list_editable=['phone']
    list_per_page = 50


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer__full_name', 'status',
                    'kind', 'session_limit', 'sessions_used', 'start_date', 'end_date']
    list_per_page = 50
    list_filter=['start_date','end_date']
    search_fields = ['customer__full_name__istartswith', 'status',
                     'kind', 'session_limit', 'sessions_used', 'start_date', 'end_date']