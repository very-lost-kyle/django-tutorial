from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import json
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.core import serializers
from django.db.models import Count
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .forms import TypeForm
from .models import pokemon
from .models import Category


class PokemonFormType(ListView):
    model = Category
    template_name = "menu/create_new_form.html"

    def post(self, request, *args, **kwargs):
        results = {
            'success': False,
            'item': {},
            'message': 'default'
        }
        status_code = 500
        try:
            # Setting local variables.
            status_code = 200
            return_id = request.POST.get('id')
            return_hide = request.POST.get('hide')

            # Getting current record.
            record = Category.objects.get(id=return_id)
            if return_hide == 'true':
                record.delete_me_bool = True
            else:
                record.delete_me_bool = False
            record.save()

            results = {
                'success': True,
                'item': model_to_dict(record),
                'message': "{} has been updated".format(record.id)
            }

        except ValueError:

            # Set local record variable to empty dictionary.
            record = {}

            # Update `results` value.
            results['item'] = model_to_dict(record),
            results['message'] = 'Failure'

        # Serialize and return `results`.
        return JsonResponse(results, status=status_code)


class PokemonType(ListView):
    model = Category
    template_name = "menu/pokemon_type.html"

    def post(self, request):

        if request.method == "POST":
            form = TypeForm(request.POST)
            # all_entries = Category.objects.all()
            # all_entries.delete()
            # print(all_entries)
            if form.is_valid():
                print('form is valid')
                post = form.save(commit=False)
                post.save()
                return redirect('menu:PokemonType')
        else:
            # print('form is not valid')
            form = TypeForm()
        return render(request, 'menu/create_new_form.html', {'form': form})


class pokemonList(ListView):
    model = pokemon


# class pokemonView(DetailView):
#     model = pokemon
#
#     def get_object(self, queryset=None):
#         id = 0
#         if 'pk' in self.kwargs:
#             id = self.kwargs['pk']
#         poke = pokemon.objects.get(pk=id)
#         return poke


class pokemonCreate(CreateView):
    def post(self, request, *args, **kwargs):
        results = {
            'success': False,
            'item': {},
            'message': 'default'
        }
        status_code = 500

        try:
            # Setting local variables.

            return_name = request.POST.get('p_name')
            return_type = request.POST.get('p_type')
            return_shiny = request.POST.get('p_shiny')
            return_level = request.POST.get('p_level')

            name_test = pokemon.objects.filter(name_text=return_name)
            # print(name_test)
            if not name_test:
                # print('empty')
                status_code = 200
                record = pokemon.objects.create(type_text=return_type,
                                                name_text=return_name,
                                                shiny_bool=return_shiny,
                                                level_int=return_level)
                return_id = record.id

                # Setting results `message`.
                message = "{} has been created".format(record.name_text)

                # Update `results` values.
                results['success'] = True,
                results['item'] = model_to_dict(record),
                results['message'] = message

            else:
                # print('not empty')
                status_code = 400
                record = {}

                # Setting results `message`.
                message = 'this pokemon already exists'

                # Update `results` value.
                results['item'] = {},
                results['message'] = message

        except ValueError:

            # Setting local variables.

            # Set local record variable to empty dictionary.
            record = {}

            # Setting results `message`.
            message = 'entry not created'

            # Update `results` value.
            results['item'] = model_to_dict(record),
            results['message'] = message

        # Serialize and return `results`.
        return JsonResponse(results, status=status_code)


class pokemonUpdate(View):
    def post(self, request, *args, **kwargs):
        results = {
            'success': False,
            'item': {},
            'message': 'default'
        }
        status_code = 500
        try:
            # Setting local variables.
            status_code = 200
            return_id = request.POST.get('id')
            return_name = request.POST.get('p_name')
            return_type = request.POST.get('p_type')
            return_shiny = request.POST.get('p_shiny')
            return_level = request.POST.get('p_level')

            name_test = pokemon.objects.filter(name_text=return_name)

            # Getting current record.
            record = pokemon.objects.get(id=return_id)

            if pokemon.objects.filter(name_text=return_name).count() == 1:
                id_check = pokemon.objects.get(name_text=return_name)
                if id_check.id == record.id:
                    # Update record values.
                    record.name_text = return_name
                    record.type_text = return_type
                    record.shiny_bool = return_shiny
                    record.level_int = return_level

                    # Save record.
                    record.save()

                    # Setting results `message`.
                    message = "{} has been updated".format(record.name_text)

                    # Update `results` values.
                    results['success'] = True,
                    results['item'] = model_to_dict(record),
                    results['message'] = message
                else:
                    status_code = 400
                    record = {}

                    # Setting results `message`.
                    message = 'this pokemon already exists'

                    # Update `results` value.
                    results['item'] = {},
                    results['message'] = message

            else:
                # Update record values.
                record.name_text = return_name
                record.type_text = return_type
                record.shiny_bool = return_shiny
                record.level_int = return_level

                # Save record.
                record.save()

                # Setting results `message`.
                message = "{} has been updated".format(record.name_text)

                # Update `results` values.
                results['success'] = True,
                results['item'] = model_to_dict(record),
                results['message'] = message


        except ValueError:

            # Set local record variable to empty dictionary.
            record = {}

            # Setting results `message`.
            message = "{} has not been updated".format(record.name_text)

            # Update `results` value.
            results['item'] = model_to_dict(record),
            results['message'] = message

        # Serialize and return `results`.
        return JsonResponse(results, status=status_code)


class pokemonDelete(View):
    def post(self, request, *args, **kwargs):
        is_delete = False
        status_code = 404
        results = {
            'success': False,
            'item': 0,
            'message': 'default'
        }
        return_id = request.POST.get('id')
        record = pokemon.objects.get(id=return_id)
        try:
            status_code = 200
            results = {
                'success': True,
                'item': record.id,
                'message': "{} has been deleted".format(record.name_text)
            }
            record.delete()
        except ValueError:
            results = {
                'item': record.id,
                'message': "an error occurred"
            }

        # return HttpResponse(json.dumps(message), content_type="application/json")
        return JsonResponse(results)
