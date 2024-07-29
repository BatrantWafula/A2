from django import forms
from .models import Bank, Branch

class BankForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ['name', 'swift_code', 'institution_number', 'description']

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name', 'transit_number', 'address', 'email', 'capacity']