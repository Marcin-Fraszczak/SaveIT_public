from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import models


class AddCategoryView(CreateView):
    model = models.Category
    template_name = 'add_category.html'
    success_url = reverse_lazy('accounts:dashboard')
    fields = ["name", "description"]

