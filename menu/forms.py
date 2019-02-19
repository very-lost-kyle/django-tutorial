from django import forms
from .models import Category


class TypeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_type',)


class SortForm(forms.Form):
    ordering = forms.IntegerField(label='sort by: ', min_value=0, max_value=7)
