from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("invoices", views.InvoiceViewSet, basename="invoices")

urlpatterns = router.urls
