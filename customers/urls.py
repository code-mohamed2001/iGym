from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('subscriptions', views.SubscriptionViewSet, basename='subscriptions')
# URLConf
urlpatterns = router.urls
