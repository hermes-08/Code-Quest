from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('api/check-email/', views.check_email_exists, name='check_email_exists'),
    
    # Main Terminal and Selection
    path('', views.index, name='home'), 
    path('quest-selector/', views.quest_selection, name='quest_selection'),
    path('python-quest/', views.python_start, name='python_start'),
    
    # This matches the {% url 'level_one_quiz' box_num %} in template
    path('python-quest/level/<int:box_num>/', views.level_one_quiz, name='level_one_quiz'),
    
    # Leaderboard Features
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard-data/', views.leaderboard_data, name='leaderboard_data'),

    # Logic & Authentication
    path('submit-quiz/', views.submit_quiz_result, name='submit_quiz'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/data/', views.leaderboard_data, name='leaderboard_data'),

    # The Map/Selection Screen
    path('python-quest/map/', views.python_start, name='python_start'),
    
    # The Quiz Level (accepts the box number as a variable)
    path('python-quest/level/<int:box_num>/', views.level_one_quiz, name='level_one_quiz'),
    
    # The AJAX endpoint for submitting answers
    path('submit-quiz/', views.submit_quiz_result, name='submit_quiz'),
]