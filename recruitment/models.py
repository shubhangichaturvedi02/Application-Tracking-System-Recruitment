from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    years_of_exp = models.FloatField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    current_salary = models.FloatField()
    expected_salary = models.FloatField()
    STATUS_CHOICES = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')

    def __str__(self):
        return self.name
