from django import forms
from .models import Category, PokemonTrainers


class PokemonTrainer(forms.ModelForm):
    class Meta:
        model = PokemonTrainers
        fields = ('name', 'num_of_pokemon', 'num_of_badges', 'is_gym_leader',)
    # name = forms.CharField(label='name', max_length=25)
    # num_of_pokemon = forms.IntegerField(label='number of pokemon', min_value=0, max_value=6)
    # num_of_badges = forms.IntegerField(label='number of badges', min_value=0, max_value=8)
    # is_gym_leader = forms.BooleanField(label='gym leader status', required=False)


class TypeForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_type',)

    def is_valid(self, **kwargs):
        super_is_valid = super(TypeForm, self).is_valid()
        # print(self.data)
        if not super_is_valid:
            # self._errors['err'] = 'form is not valid'
            return super_is_valid
        else:
            # print(self.data.__getitem__('category_type'))
            test_unique = Category.objects.filter(category_type=self.data.__getitem__('category_type')).exists()
            if test_unique:
                # print('exists=true')
                self._errors['err'] = 'category already exists'
                # raise forms.ValidationError('category already exists')
                return False
            else:
                # print('exists=false')
                return True


class SortForm(forms.Form):
    ordering = forms.IntegerField(label='sort by: ', min_value=0, max_value=7)
