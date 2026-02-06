# app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassroomViewSet

from . import views

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet, basename='classroom')

urlpatterns = [
    path('api/', include(router.urls)),

    path('api/get-faces/', views.get_faces, name='get-faces'),
    path('api/register-face/', views.register_face, name='register_face'),
]
