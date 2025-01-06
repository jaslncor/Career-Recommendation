from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend', views.recommend, name='recommend'),
    path('pred/', views.pred, name='pred'),
    path('submit_career_selection/', views.submit_career_selection, name='submit_career_selection'),
]

