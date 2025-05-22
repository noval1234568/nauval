import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Load Data
df = pd.read_csv('student_performance_dataset.csv')

# 2. Buat label kategori performa berdasarkan rata_rata_nilai
def kategori_performa(nilai):
    if nilai >= 85:
        return "Berprestasi"
    elif nilai >= 70:
        return "Cukup"
    else:
        return "Kurang"

df['kategori'] = df['rata_rata_nilai'].apply(kategori_performa)

# 3. Feature engineering: encode gender dan hitung umur
df['gender_enc'] = df['gender'].map({'L': 0, 'P': 1})
df['dob'] = pd.to_datetime(df['dob'])
df['umur'] = (pd.Timestamp('today') - df['dob']).dt.days // 365

# 4. Pisahkan fitur dan label
features = ['gender_enc', 'umur', 'rata_rata_nilai']
X = df[features]
y = df['kategori']

# 5. Split data menjadi data latih dan uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Training model Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# 7. Evaluasi model
y_pred = clf.predict(X_test)
print("Akurasi:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# 8. Simpan model untuk digunakan di aplikasi lain
joblib.dump(clf, 'student_performance_classifier.pkl')