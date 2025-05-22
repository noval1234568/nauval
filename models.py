from django.db import models

class ActivityType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'activity_type'

    def __str__(self):
        return self.type_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.course_name

class Student(models.Model):
    stu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    dob = models.DateField()

    class Meta:
        db_table = 'student'

    def __str__(self):
        return self.name

class CourseActivity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ActivityType, on_delete=models.SET_NULL, null=True, db_column='type_id')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, db_column='course_id')
    activity_name = models.CharField(max_length=100, null=True, blank=True)
    activity_start_date = models.DateTimeField(null=True, blank=True)
    activity_end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'course_activity'

    def __str__(self):
        return self.activity_name or f'Activity {self.activity_id}'

class Enrollment(models.Model):
    enroll_id = models.AutoField(primary_key=True)
    stu = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, db_column='stu_id')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, db_column='course_id')
    grade = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'enrollment'

    def __str__(self):
        return f"{self.stu} - {self.course}"

class StudentActivityLog(models.Model):
    stu = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='stu_id')
    activity = models.ForeignKey(CourseActivity, on_delete=models.CASCADE, db_column='activity_id')
    activity_start = models.DateTimeField()
    activity_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'student_activity_log'
        unique_together = ('stu', 'activity', 'activity_start')

    def __str__(self):
        return f"{self.stu} - {self.activity} at {self.activity_start}"