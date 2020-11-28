from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView

from catalog.models import Car


class CarList(ListView):
    model = Car
    template_name = 'car-list.html'

    def get_queryset(self):
        q_set = Car.objects.all()
        params = self.request.GET.dict()

        # search for a big form with many filters
        prod = params.get('producer')
        mod = params.get('model')
        year = params.get('release_year')
        trans = params.get('transmission')
        color = params.get('color')

        if prod:
            q_set = q_set.filter(producer__icontains=prod)

        if mod:
            q_set = q_set.filter(model__icontains=mod)

        if year:
            q_set = q_set.filter(release_year__icontains=year)

        if trans:
            q_set = q_set.filter(transmission__icontains=trans)

        if color:
            q_set = q_set.filter(color__icontains=color)

        # search for simple form
        if params.get('search'):
            val = params.get('search')
            q_set = Car.objects.filter(
                Q(producer__icontains=val)
                | Q(model__icontains=val)
                | Q(release_year__icontains=val)
                | Q(transmission__icontains=val)
                | Q(color__icontains=val)
            )

        return q_set