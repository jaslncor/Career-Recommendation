import pickle
from .models import Recommendation

def generate_recommendations(profile):
    # Load the trained ML model
    with open('path/to/recommendation_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    
    # Use model to predict recommendations (this may vary based on your model and features)
    recommended_careers = model.predict([[profile.age, profile.interests, profile.career_goal]])
    
    # Save recommendations to the database
    for career in recommended_careers:
        Recommendation.objects.create(user_profile=profile, recommended_career=career, description="Career Description")
