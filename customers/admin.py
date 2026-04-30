from django.contrib import admin

from .models import Customer, Subscription


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'barcode', 'phone', 'id_number']
    list_per_page = 50


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer__full_name', 'status',
                    'kind', 'session_limit', 'sessions_used', 'start_date', 'end_date']
    list_per_page = 50