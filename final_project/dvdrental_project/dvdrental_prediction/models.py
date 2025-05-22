from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ActivityType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.type_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.course_name

class CourseActivity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    activity_start_date = models.DateTimeField()
    activity_end_date = models.DateTimeField()
    
    def __str__(self):
        return self.activity_name

class Student(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    stu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()
    
    def __str__(self):
        return self.name

class Enrollment(models.Model):
    enroll_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField()
    
    def __str__(self):
        return f"{self.student} in {self.course}"

class StudentActivityLog(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    activity = models.ForeignKey(CourseActivity, on_delete=models.CASCADE)
    activity_start = models.DateTimeField()
    activity_end = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student} - {self.activity}"

class MLModel(models.Model):
    MODEL_TYPES = [
        ('classification', 'Classification'),
        ('regression', 'Regression'),
        ('clustering', 'Clustering'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    model_file = models.FileField(upload_to='ml_models/')
    accuracy = models.FloatField(null=True, blank=True)
    precision = models.FloatField(null=True, blank=True)
    recall = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return self.namec