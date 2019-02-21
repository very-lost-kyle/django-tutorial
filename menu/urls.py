from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('pokemon-trainers', views.PokemonTrainers.as_view(), name='pokemon-trainers'),
    path('category-update/<int:pk>', views.CategoryUpdate.as_view(), name='category-update'),
    path('type', views.PokemonType.as_view(), name='PokemonType'),
    path('typeForm', views.PokemonFormType.as_view(), name='PokemonFormType'),
    path('', views.PokemonList.as_view(), name='pokemon_form'),
    path('new', views.PokemonCreate.as_view(), name='pokemon_new'),
    path('edit/', views.PokemonUpdate.as_view(), name='pokemon_edit'),
    path('delete/<int:pk>', views.PokemonDelete.as_view(), name='pokemon_delete'),

]
