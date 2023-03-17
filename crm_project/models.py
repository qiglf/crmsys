from django.db import models
from django.db.models import Q

#TODO: add companyname and connect with candidate, in company
# there must be positions they need and their reqrmnts for candidate.

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)
  phone = models.CharField(null=True, max_length=255)
  #joined_date = models.DateField(null=True)
  email = models.EmailField(null=True)
  country = models.CharField(max_length=255, null=True)
  id = models.IntegerField(primary_key=True)
  education = models.CharField(max_length=255, null=True)
  desired_position = models.CharField(max_length=255, null=True)
  amount_of_workplaces = models.IntegerField(null=True)
  total_years_of_exp = models.IntegerField(null=True)
  hire_success = models.FloatField(null=True)

  def __str__(self):
    return f"{self.firstname} {self.lastname} ({self.id})"

class Work(models.Model):
  id = models.IntegerField(default=1, primary_key=True)
  mId = models.ForeignKey(Member, default=1, on_delete=models.SET_DEFAULT)
  company_name = models.CharField(max_length=255, null=True)
  years = models.FloatField(null=True)
  level = models.IntegerField(null=True)
  salary = models.IntegerField(null=True)
  reference = models.BooleanField(null=True)





#def __str__(self):
  #return self.lastname
