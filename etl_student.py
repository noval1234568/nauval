from django.core.management.base import BaseCommand
import pandas as pd
from django.db.models import Avg, Count, Sum
from dvdrental_prediction import Student, Enrollment, CourseActivity, StudentActivityLog
import numpy as np

class Command(BaseCommand):
    help = "ETL = Extract student performance data and save as csv"
    
    def handle(self, *args, **kwargs):
        data = []
        
        for student in Student.objects.all():
            # Get all enrollments for the student
            enrollments = Enrollment.objects.filter(stu_id=student.stu_id)
            
            # Calculate performance metrics
            total_grades = enrollments.aggregate(total=Sum('grade'))['total'] or 0
            course_count = enrollments.count()
            average_grade = total_grades / course_count if course_count > 0 else 0
            average_grade = np.float32(average_grade)
            
            # Get activity participation data
            activity_logs = StudentActivityLog.objects.filter(stu_id=student.stu_id)
            activity_count = activity_logs.count()
            
            # Calculate average activity duration
            if activity_count > 0:
                durations = [(log.activity_end - log.activity_start).total_seconds() / 60 
                           for log in activity_logs if log.activity_end]
                avg_duration = np.mean(durations) if durations else 0
            else:
                avg_duration = 0
                
            avg_duration = np.float32(avg_duration)
            
            data.append({
                'student_id': student.stu_id,
                'name': student.name,
                'email': student.email,
                'gender': student.gender,
                'dob': student.dob,
                'total_grade': total_grades,
                'course_count': course_count,
                'average_grade': np.round(average_grade, 2),
                'activity_count': activity_count,
                'avg_activity_duration': np.round(avg_duration, 2)
            })
        
        df = pd.DataFrame(data)
        df.to_csv('student_performance_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Student Performance Dataset saved to CSV.'))
