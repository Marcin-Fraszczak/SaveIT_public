from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from . import models
from . import forms


class AddCategoryView(View):

    def post(self, request):
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            exists = models.Category.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "Category already exists")
            else:
                form.save()
                messages.success(request, "Category successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_category')

    def get(self, request):

        form = forms.CategoryForm
        return render(request=request, template_name='transactions/add_category.html', context={"form": form})


class AddCounterpartyView(View):

    def post(self, request):
        form = forms.CounterpartyForm(request.POST)
        if form.is_valid():
            exists = models.Counterparty.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "Counterparty already exists")
            else:
                form.save()
                messages.success(request, "Counterparty successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_counterparty')

    def get(self, request):

        form = forms.CounterpartyForm
        return render(request=request, template_name='transactions/add_counterparty.html', context={"form": form})


class ListCategoryView(ListView):
    model = models.Category
    template_name = 'transactions/list_category.html'


class ListCounterpartyView(ListView):
    model = models.Counterparty
    template_name = 'transactions/list_counterparty.html'


class ListWalletView(ListView):
    model = models.Wallet
    template_name = 'transactions/list_wallet.html'

