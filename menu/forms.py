from django import forms
from .models import Category


class TypeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_type',)
