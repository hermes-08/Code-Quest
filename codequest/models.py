from django.db import models
from django.contrib.auth.models import User

class Recruit(models.Model):
    # Links to Django's built-in User (Email/Password)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Extra data
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    
    # Quest progress
    is_python_unlocked = models.BooleanField(default=True)
    is_java_unlocked = models.BooleanField(default=False)
    is_cpp_unlocked = models.BooleanField(default=False)

    exp = models.IntegerField(default=0)
    unlocked_level = models.IntegerField(default=1) 

    # Stores the list of level IDs completed
    completed_levels = models.JSONField(default=list)

    # EXP REQUIREMENTS
    @property
    def exp_required(self):
        """Calculates the total EXP needed to reach the NEXT level."""
        # Level 1 needs 150 EXP, Level 2 needs 200 EXP, (50 EXP increase per level)
        return 100 + (self.unlocked_level * 50)

    @property
    def progress_percentage(self):
        """Calculates 0-100% progress toward the next level for the UI bar."""
        if self.unlocked_level >= 8 and self.exp >= self.exp_required:
            return 100
        return round((self.exp / self.exp_required) * 100, 1)

    # RANKING SYSTEM
    @property
    def rank(self):
        """
        Matches the Round Unlock logic: 1-3 (Novice), 4-6 (Warrior), 7+ (Architect)
        """
        if self.unlocked_level >= 7:
            return "Elite Architect"
        elif self.unlocked_level >= 4:
            return "Code Warrior"
        else:
            return "Novice"

    @property
    def total_missions_cleared(self):
        """Returns the total count of unique levels finished."""
        return len(self.completed_levels)

    def __str__(self):
        return f"{self.full_name} ({self.rank})"