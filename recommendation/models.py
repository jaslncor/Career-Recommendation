from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    interests = models.TextField()
    career_goal = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username

class Recommendation(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recommended_career = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.recommended_career

