from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.http import JsonResponse
from .forms import TypeForm, SortForm
from .models import pokemon
from .models import Category
from django.core.exceptions import ValidationError


class CategoryUpdate(View):
    model = Category
    template_name = "menu/pokemon_type.html"

    def post(self, request, *args, **kwargs):

        if request.method == "POST":
            is_delete = False
            status_code = 500
            results = {
                'success': False,
                'item': {},
                'message': 'default'
            }
            try:
                return_id = request.POST.get('id')
                delete_bool = request.POST.get('delete_bool')
                return_hide = request.POST.get('hide')
                record = Category.objects.get(id=return_id)
                status_code = 200
                results = {
                    'success': True,
                    'item': record.id,
                    'message': ""
                }
                if delete_bool == 'true':
                    results['message'] = "{} has been deleted".format(record.category_type)
                    record.delete()
                else:
                    if return_hide == 'true':
                        record.delete_me_bool = True
                    else:
                        record.delete_me_bool = False
                    results['message'] = "{} has been updated".format(record.category_type)
                    record.save()
            except ValueError:
                results = {
                    'item': {},
                    'message': "an error occurred"
                }
            return JsonResponse(results)


class PokemonFormType(ListView):
    model = Category
    template_name = "menu/create_new_form.html"

    def get(self, request):
        form = TypeForm()
        data = {
            'err': [],
            'form': form
        }
        return render(request, 'menu/create_new_form.html', {'data': data})

    def post(self, request, *args, **kwargs):
        errors = []
        form = TypeForm(request.POST)

        if form.is_valid():
            if 'err' in form._errors:
                errors.append(form._errors['err'])
            post = form.save(commit=False)
            post.save()
            errors = []
            return redirect('menu:PokemonType')
        else:
            if 'err' in form._errors:
                errors.append(form._errors['err'])
            form = TypeForm()
            data = {
                'err': errors,
                'form': form
            }
            errors = []
            return render(request, 'menu/create_new_form.html', {'data': data})


class PokemonType(ListView):
    model = Category
    template_name = "menu/pokemon_type.html"


class PokemonList(ListView):
    queryset = pokemon.objects.all().select_related('foreign_type')
    context_object_name = 'poke'
    template_name = 'menu/pokemon_list.html'

    sort = {
        0: ('name_text',),
        1: ('-name_text',),
        2: ('foreign_type__category_type', 'name_text'),
        3: ('-foreign_type__category_type', 'name_text'),
        4: ('level_int',),
        5: ('-level_int',),
        6: ('shiny_bool', 'name_text'),
        7: ('-shiny_bool', 'name_text'),
        8: ('id',),
    }

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PokemonList, self).get_context_data(**kwargs)
        context['pokemons_types'] = Category.objects.filter(delete_me_bool=False)
        ordering = self.sort[int(self.request.GET.get('ordering', '8'))]
        context['object_list'] = context['object_list'].order_by(*ordering)
        return context


class PokemonCreate(CreateView):
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
            if not name_test:
                status_code = 200
                record = pokemon.objects.create(foreign_type_id=return_type,
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


class PokemonUpdate(View):
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
                    record.foreign_type_id = return_type
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
                record.foreign_type_id = return_type
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
            message = 'record does not exist?'

            # Update `results` value.
            results['item'] = record,
            results['message'] = message

        # Serialize and return `results`.
        return JsonResponse(results, status=status_code)


class PokemonDelete(View):
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
        return JsonResponse(results)
