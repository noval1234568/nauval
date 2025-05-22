from django.core.management.base import BaseCommand
import pandas as pd
from django.db.models import Sum
from dvdrental_prediction.models import Student, StudentActivityLog, ActivityType, CourseActivity, Course, Enrollment
import numpy as np

class Command(BaseCommand):
    help = "ETL: Extract study-case data and sav as CSV"

def handle(self, *args, **kwargs):
    data = []
    for student in Student.objects.all():
        enrollments = Enrollment.objects.filter(stu_id=student.stu_id)
        total_grades = enrollments.aggregate(total=Sum('grade'))['total'] or 0
        course_count = enrollments.count()
        average_grade = total_grades / course_count if course_count > 0 else 0
        average_grade = np.float32(average_grade)
    
    data.append({
                'student_id': student.stu_id,
                'name': student.name,
                'email': student.email,
                'gender': student.gender,
                'dob': student.dob,
                'total_grade': total_grades,
                'course_count': course_count,
                'average_grade': np.round(average_grade, 2)
    })

    df = pd.DataFrame(data)
    df.to_csv('etl_student.csv', index=False)
    self.stdout.write(self.style.SUCCESS('ETL completed and CSV file saved.'))
