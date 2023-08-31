from django.db import models

# Create your models here.
class companiesModel(models.Model):
    unique_number = models.IntegerField()
    name = models.CharField(max_length=500)
    domain = models.CharField(max_length=500, null=True, blank=True)
    year_founded = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    size_range = models.CharField(max_length=100)
    locality = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    linkedin_url = models.CharField(max_length=1000, null=True, blank=True)
    current_employee_estimate = models.IntegerField(null=True, blank=True)
    total_employee_estimate = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name