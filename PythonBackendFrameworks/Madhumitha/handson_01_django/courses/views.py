from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Department, Course, Student, Enrollment
from .serializers import DepartmentSerializer, CourseSerializer, StudentSerializer, EnrollmentSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset         = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'], url_path='students')
    def enrolled_students(self, request, pk=None):
        course   = self.get_object()
        students = Student.objects.filter(enrollments__course=course)
        return Response(StudentSerializer(students, many=True).data)

class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.all()
    serializer_class = StudentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset         = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset         = Department.objects.all()
    serializer_class = DepartmentSerializer