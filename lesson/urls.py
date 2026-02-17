# app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassroomViewSet,RegisterViewSet,get_user_data,StudentAttendanceViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from . import views

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'attendance', StudentAttendanceViewSet, basename='attendance')

urlpatterns = [
    path('me/',get_user_data,name='me'),
    path('register/',RegisterViewSet.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login-token'),
    path('refresh',TokenRefreshView.as_view(),name='refresh-token'),

    path('api/', include(router.urls)),

    path('api/get-faces/', views.get_faces, name='get-faces'),
    path('api/register-face/', views.register_face, name='register_face'),
]
