from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('courses',     views.CourseViewSet)
router.register('students',    views.StudentViewSet)
router.register('enrollments', views.EnrollmentViewSet)
router.register('departments', views.DepartmentViewSet)

urlpatterns = [path('', include(router.urls))]