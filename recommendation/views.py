from django.http import JsonResponse
from django.shortcuts import render
import pickle
import numpy as np
import pandas as pd

import os
from django.conf import settings
import pickle

scaler_path = os.path.join(settings.BASE_DIR, 'recommendation', 'Models', 'scaler.pkl')
scaler = pickle.load(open(scaler_path, 'rb'))
model_path = os.path.join(settings.BASE_DIR, 'recommendation', 'Models', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

# Load model and scaler

class_names = ['Lawyer', 'Doctor', 'Government Officer', 'Artist', 'Unknown',
               'Software Engineer', 'Teacher', 'Business Owner', 'Scientist',
               'Banker', 'Writer', 'Accountant', 'Designer',
               'Construction Engineer', 'Game Developer', 'Stock Investor',
               'Real Estate Developer']

# Sample dataset for career options
data = {
    "Career Option": ["Accountant", "Artist", "Banker", "Business Owner", 
                      "Construction Engineer", "Designer", "Doctor", 
                      "Game Developer", "Government Officer", "Lawyer", 
                      "Real Estate Developer", "Scientist", "Software Engineer", 
                      "Stock Investor", "Teacher", "Writer"],
    "Top Colleges in India": [
        "Institute of Chartered Accountants of India, Delhi University", 
        "National Institute of Fine Arts, Delhi College of Art", 
        "Indian Institute of Banking & Finance, Delhi University", 
        "Indian Institute of Management (IIM), Xavier School of Management", 
        "Indian Institute of Technology (IIT), National Institute of Technology (NIT)", 
        "National Institute of Design, National Institute of Fashion Technology", 
        "All India Institute of Medical Sciences (AIIMS), Christian Medical College (CMC)", 
        "IIT Bombay, Vellore Institute of Technology", 
        "Lal Bahadur Shastri National Academy of Administration, Delhi University", 
        "National Law School of India University, National Academy of Legal Studies and Research", 
        "Indian School of Business (ISB), RICS School of Built Environment", 
        "Indian Institute of Science (IISc), Tata Institute of Fundamental Research (TIFR)", 
        "IITs, IIIT Hyderabad", 
        "Indian Institute of Capital Markets, NSE Academy", 
        "Tata Institute of Social Sciences (TISS), Banaras Hindu University", 
        "JNU, Delhi University"
    ],
    "Entrance Exams": [
        "CA Foundation, DU JAT", "NID DAT, UCEED", "IBPS, SBI PO", 
        "CAT, XAT", "JEE Main, JEE Advanced", "NID DAT, NIFT Entrance", 
        "NEET", "UCEED, VITEEE", "UPSC CSE", "CLAT, AILET", 
        "CAT, GMAT", "GATE, TIFR GS", "JEE Main, JEE Advanced", 
        "NSE NCFM, CFA", "TISSNET, BHU UET", "JNU Entrance Exam, DUET"
    ]
}
df = pd.DataFrame(data)

# Function for recommendations
def Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                    weekly_self_study_hours, math_score, history_score, physics_score,
                    chemistry_score, biology_score, english_score, geography_score,
                    total_score, average_score):
    # Encode categorical variables
    gender_encoded = 1 if gender.lower() == 'female' else 0
    part_time_job_encoded = 1 if part_time_job else 0
    extracurricular_activities_encoded = 1 if extracurricular_activities else 0

    # Create a feature array
    feature_array = np.array([[gender_encoded, part_time_job_encoded, absence_days, extracurricular_activities_encoded,
                               weekly_self_study_hours, math_score, history_score, physics_score,
                               chemistry_score, biology_score, english_score, geography_score, total_score,
                               average_score]])

    # Convert to DataFrame with appropriate column names
    feature_names = [
        'gender', 'part_time_job', 'absence_days', 'extracurricular_activities',
        'weekly_self_study_hours', 'math_score', 'history_score', 'physics_score',
        'chemistry_score', 'biology_score', 'english_score', 'geography_score',
        'total_score', 'average_score'
    ]
    feature_df = pd.DataFrame(feature_array, columns=feature_names)

    # Scale features
    scaled_features = scaler.transform(feature_df)

    # Predict using the model
    probabilities = model.predict_proba(scaled_features)

    # Get top three predicted classes along with their probabilities
    top_classes_idx = np.argsort(-probabilities[0])[:3]
    top_classes_names_probs = [(class_names[idx], probabilities[0][idx]) for idx in top_classes_idx]

    return top_classes_names_probs

# Home page
def home(request):
    return render(request, 'home.html')

# Recommendation form page
def recommend(request):
    return render(request, 'recommend.html')

# Prediction and recommendation results
def pred(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        part_time_job = request.POST.get('part_time_job') == 'true'
        absence_days = int(request.POST.get('absence_days'))
        extracurricular_activities = request.POST.get('extracurricular_activities') == 'true'
        weekly_self_study_hours = int(request.POST.get('weekly_self_study_hours'))
        math_score = int(request.POST.get('math_score'))
        history_score = int(request.POST.get('history_score'))
        physics_score = int(request.POST.get('physics_score'))
        chemistry_score = int(request.POST.get('chemistry_score'))
        biology_score = int(request.POST.get('biology_score'))
        english_score = int(request.POST.get('english_score'))
        geography_score = int(request.POST.get('geography_score'))
        total_score = float(request.POST.get('total_score'))
        average_score = float(request.POST.get('average_score'))

        recommendations = Recommendations(gender, part_time_job, absence_days, extracurricular_activities,
                                          weekly_self_study_hours, math_score, history_score, physics_score,
                                          chemistry_score, biology_score, english_score, geography_score,
                                          total_score, average_score)

        return render(request, 'results.html', {'recommendations': recommendations})

# Career selection
def submit_career(request):
    if request.method == 'POST':
        selected_careers = request.POST.getlist('careers')
        return JsonResponse({'selected': selected_careers})

# Career options recommendations
def submit_career_selection(request):
    if request.method == 'POST':
        selected_careers = request.POST.getlist('career_options')
        recommendations = []

        for career in selected_careers:
            result = df[df['Career Option'] == career]
            if not result.empty:
                recommendations.append({
                    'career': career,
                    'colleges': result['Top Colleges in India'].values[0],
                    'exams': result['Entrance Exams'].values[0]
                })

        return render(request, 'recommendations.html', {'recommendations': recommendations})
