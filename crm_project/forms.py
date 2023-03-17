from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'phone', 'email', 'country', 'education', 'desired_position', 'amount_of_workplaces', 'total_years_of_exp', 'hire_success']
