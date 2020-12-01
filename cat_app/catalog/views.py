from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Car
from catalog.forms import SearchForm, OneRowSearch


class CarList(ListView):
    model = Car
    template_name = 'car-list.html'

    def get_context_data(self, **kwargs):
        context = super(CarList, self).get_context_data( **kwargs)
        context['optional_search'] = SearchForm()
        context['one_row_search'] = OneRowSearch()

        return context

    def get_queryset(self):
        q_set = Car.objects.all()
        params = self.request.GET.dict()

        # search for the homework
        if params.get('search'):
            val = params.get('search')
            q_set = Car.objects.filter(
                Q(producer__icontains=val)
                | Q(model__icontains=val)
                | Q(release_year__icontains=val)
                | Q(transmission__icontains=val)
                | Q(color__icontains=val)
            )
        else:
            # search for a big form with many filters
            prod = params.get('producer')
            mod = params.get('model')
            year = params.get('release_year')
            transmission = params.get('transmission')
            color = params.get('color')

            if prod:
                q_set = q_set.filter(producer__icontains=prod)

            if mod:
                q_set = q_set.filter(model__icontains=mod)

            if year:
                q_set = q_set.filter(release_year__icontains=year)

            if transmission and not transmission == 'All':
                q_set = q_set.filter(transmission__icontains=transmission)

            if color:
                q_set = q_set.filter(color__icontains=color)

        return q_set