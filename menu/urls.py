from django.urls import path

from . import views

app_name = 'menu'
urlpatterns = [
    path('type', views.PokemonType.as_view(), name='PokemonType'),
    path('typeForm', views.PokemonFormType.as_view(), name='PokemonFormType'),
    path('', views.pokemonList.as_view(), name='pokemon_form'),
    # path('view/<int:pk>', views.pokemonView.as_view(), name='pokemon_view'),
    path('new', views.pokemonCreate.as_view(), name='pokemon_new'),
    path('edit/', views.pokemonUpdate.as_view(), name='pokemon_edit'),
    path('delete/', views.pokemonDelete.as_view(), name='pokemon_delete'),

]
