from django.urls import path

from . import views

# URLConf
urlpatterns = [
    path('', views.customer_list),
    path('subs/', views.subscription_list),
    path('<str:id>/', views.customer_datail),
]
