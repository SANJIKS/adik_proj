from django.urls import path
from .views import SetUserRating, CustomUserViewSet


urlpatterns = [
    path('users/', SetUserRating.as_view(), name='user-rating'),
    path('register/contractor/', CustomUserViewSet.as_view({'post': 'create_contractor'}), name='contractor-registration'),
]