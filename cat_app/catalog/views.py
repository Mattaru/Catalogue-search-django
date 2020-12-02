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
            request_filters = Q()
            for key, value in params.items():
                if value and not value == 'All':
                    request_filters &= Q(**{f'{key}__icontains': value})
            q_set = Car.objects.filter(request_filters)

        return q_set