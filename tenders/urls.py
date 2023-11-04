from rest_framework.routers import DefaultRouter
from .views import TenderViewSet, TenderApplicationViewSet

router = DefaultRouter()
router.register(r'tenders', TenderViewSet)
router.register(r'tender-applications', TenderApplicationViewSet)

urlpatterns = router.urls
