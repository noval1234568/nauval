from django.core.management.base import BaseCommand
import pandas as pd
from django.db.models import Avg
from dvdrental_prediction.models import Student, Enrollment
import numpy as np

class Command(BaseCommand):
    help = "ETL = Extract student data, calculate average grades and save to CSV"

    def handle(self, *args, **kwargs):
        data = []

        avg_grades = Enrollment.objects.values('stu_id').annotate(rata_rata_nilai=Avg('grade'))
        print("Avg grades query result:", list(avg_grades))

        students = {student.stu_id: student for student in Student.objects.all()}
        print("Students data:", students)

        for avg in avg_grades:
            student_id = avg['stu_id']
            rata_rata_nilai = avg['rata_rata_nilai']
            student = students.get(student_id)

            if student:
                data.append({
                    'stu_id': student.stu_id,
                    'gender': student.gender,
                    'dob': student.dob,
                    'rata_rata_nilai': np.float32(rata_rata_nilai),
                })
            else:
                print(f"Student with ID {student_id} not found in students dictionary")

        print(f"Jumlah data yang akan disimpan: {len(data)}")

        df = pd.DataFrame(data)
        print(df.head())

        df.to_csv('student_performance_dataset.csv', index=False)
        self.stdout.write(self.style.SUCCESS('Student Performance Dataset saved to CSV.'))
