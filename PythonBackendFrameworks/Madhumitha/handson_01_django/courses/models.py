from django.db import models

class Department(models.Model):
    name         = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100, blank=True)
    budget       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    def __str__(self): return self.name

class Course(models.Model):
    name       = models.CharField(max_length=150)
    code       = models.CharField(max_length=20, unique=True)
    credits    = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    def __str__(self): return f"{self.code} — {self.name}"

class Student(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(unique=True)
    department      = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_year = models.IntegerField()
    def __str__(self): return f"{self.first_name} {self.last_name}"

class Enrollment(models.Model):
    student         = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course          = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    grade           = models.CharField(max_length=2, null=True, blank=True)
    class Meta:
        unique_together = [['student', 'course']]