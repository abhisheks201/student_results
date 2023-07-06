from django.db import models


class User(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    hall_ticket = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    school = models.CharField(max_length=250)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'User'


class Marks(models.Model):
    user = models.ForeignKey(User, related_name='marks', on_delete=models.CASCADE)
    telugu = models.CharField(max_length=50)
    hindi = models.CharField(max_length=50)
    english = models.CharField(max_length=100)
    maths = models.CharField(max_length=50)
    science = models.CharField(max_length=100)
    social = models.CharField(max_length=100)

    class Meta:
        db_table = 'Marks'

