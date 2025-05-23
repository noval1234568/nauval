from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib
import os

class Command(BaseCommand):
    help = 'Train model Random Forest dari dataset CSV hasil ETL'

    def handle(self, *args, **kwargs):
        csv_path = 'activity_effectiveness_dataset.csv'

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"File {csv_path} tidak ditemukan. Jalankan ETL dulu!"))
            return

        self.stdout.write("Membaca dataset dari CSV...")
        df = pd.read_csv(csv_path)

        # Encode categorical feature activity_type_name
        le = LabelEncoder()
        df['activity_type_encoded'] = le.fit_transform(df['activity_type_name'])

        # Fitur dan target
        X = df[['gender_encoded', 'age', 'activity_type_encoded', 'total_duration_minutes']]
        y = df['success']

        # Split data train-test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.stdout.write("Training model Random Forest...")
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        self.stdout.write("Menguji model pada data test...")
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        cr = classification_report(y_test, y_pred)

        self.stdout.write(self.style.SUCCESS(f"Accuracy: {acc:.4f}"))
        self.stdout.write(f"Confusion Matrix:\n{cm}")
        self.stdout.write(f"Classification Report:\n{cr}")

        # Simpan model
        model_path = 'rf_activity_success_model.joblib'
        joblib.dump(model, model_path)
        self.stdout.write(self.style.SUCCESS(f"Model tersimpan di '{model_path}'"))
