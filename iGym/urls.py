"""
URL configuration for iGym project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = 'iGym Admin'

admin.site.index_title = "Admin Dashboard"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('BackEnd/BrowseCustomers/', include('customers.urls')),
    path('BackEnd/BrowseCheckIns/', include('checkins.urls')),
    path('BackEnd/BrowsePayments/', include('payments.urls')),
    path('BackEnd/auth/', include('djoser.urls')),
    path('BackEnd/auth/', include('djoser.urls.jwt')),
] + debug_toolbar_urls()


# /users/ sign up

# /users/me/

# /users/resend_activation/

# /users/set_password/

# /users/reset_password/

# /users/reset_password_confirm/

# /users/set_username/

# /users/reset_username/

# /users/reset_username_confirm/


# /jwt/create / (JSON Web Token Authentication) login

# /jwt/refresh / (JSON Web Token Authentication)

# /jwt/verify / (JSON Web Token Authentication)
