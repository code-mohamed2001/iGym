from django.contrib import admin

from .models import CheckIn


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['customer__full_name',
                    'visit_type', 'created_at']
    list_per_page=50