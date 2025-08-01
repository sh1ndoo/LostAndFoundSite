from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from apps.things.forms import ThingForm
from apps.things.mixins import OwnerRequiredMixin
from apps.things.models import Thing
from apps.things.service import *

class IndexView(ListView):
    template_name = "base.html"
    context_object_name = 'things'
    model = Thing


class CreateThingView(LoginRequiredMixin, CreateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things/thing_create.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("things:index")


class SearchThingView(View):
    template_name = "things/thing_list.html"
    context_object_name = 'things'

    def get(self, request):
        status = request.GET.get('status', None)
        query = request.GET.get('q', '')
        sort = request.GET.get('sort', '')
        things = get_things_by_params(status=status, query=query, sort=sort)
        return render(request, self.template_name, {self.context_object_name: things, 'status': status, 'q': query})

class DetailThingView(DetailView):
    model = Thing
    template_name = "things/detail_thing.html"
    context_object_name = 'thing'


class EditThingView(OwnerRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Thing
    form_class = ThingForm
    template_name = 'things/thing_edit.html'


class DeleteThingView(OwnerRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Thing
    template_name = 'things/thing_delete.html'
    success_url = reverse_lazy("things:index")


def view_404(request, exception):
    return render(request, '404.html', status=404)

def view_500(request):
    return render(request, '500.html', status=500)
