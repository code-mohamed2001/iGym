from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('', views.customer_list),
    path('<int:id>/', views.customer_datail),
    
]
