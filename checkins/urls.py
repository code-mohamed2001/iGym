from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("", views.CheckInViewSet, basename="checkins")

urlpatterns = router.urls
