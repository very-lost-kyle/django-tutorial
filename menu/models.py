from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_type = models.CharField(max_length=50)
    delete_me_bool = models.BooleanField(default=False)

    def __str__(self):
        return self.category_type

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Category._meta.fields]


class pokemon(models.Model):
    type_text = models.CharField(max_length=10)
    name_text = models.CharField(max_length=50)
    shiny_bool = models.BooleanField(default=False)
    level_int = models.IntegerField(default=1)
    foreign_type = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_text

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in pokemon._meta.fields]

    def get_absolute_url(self):
        return reverse('pokemon_edit', kwargs={'pk': self.pk})

    def sort(self):
        return pokemon.objects.order_by(self.name_text)
