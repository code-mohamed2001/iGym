from django.contrib import admin

from .models import CheckIn


@admin.register(CheckIn)
class CheckInAdmin():
    pass
