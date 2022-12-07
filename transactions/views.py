from django.contrib import messages
from django.contrib.auth import get_user_model, get_user
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import CreateView, ListView
from . import models
from . import forms


class AddTransactionView(View):
    def post(self, request):
        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            wallets = list(form.cleaned_data.get("wallet"))
            transaction = form.save(commit=False)
            transaction.owner = get_user(request)
            transaction.save()
            transaction.wallet.set(wallets)
            messages.success(request, "Transaction successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_transaction')

    def get(self, request):
        form = forms.TransactionForm
        return render(request=request, template_name='transactions/add_transaction.html', context={"form": form})


class ModifyTransactionView(View):
    def post(self, request, pk):
        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            transaction = get_object_or_404(models.Transaction, pk=pk)
            transaction.date = form.cleaned_data.get("date")
            transaction.value = form.cleaned_data.get("value")
            transaction.is_profit = form.cleaned_data.get("is_profit")
            transaction.notes = form.cleaned_data.get("notes")
            transaction.category = form.cleaned_data.get("category")
            transaction.counterparty = form.cleaned_data.get("counterparty")
            transaction.save()
            wallets = list(form.cleaned_data.get("wallet"))
            transaction.wallet.set(wallets)
            messages.success(request, "Transaction successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_transaction')

    def get(self, request, pk):
        user = get_user(request)
        transaction = get_object_or_404(models.Transaction, pk=pk)
        if user != transaction.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        form = forms.TransactionForm(instance=transaction)
        return render(request=request, template_name='transactions/modify_transaction.html',
                      context={"form": form, "object": transaction})




class AddCategoryView(View):
    def post(self, request):
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            exists = models.Category.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "Category already exists")
            else:
                category = form.save(commit=False)
                category.owner = get_user(request)
                category.save()
                messages.success(request, "Category successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_category')

    def get(self, request):
        form = forms.CategoryForm
        return render(request=request, template_name='transactions/add_category.html', context={"form": form})


class ModifyCategoryView(View):
    def post(self, request, pk):
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            category = get_object_or_404(models.Category, pk=pk)
            category.name = form.cleaned_data.get("name")
            category.description = form.cleaned_data.get("description")
            category.save()
            messages.success(request, "Category successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_category')

    def get(self, request, pk):
        user = get_user(request)
        category = get_object_or_404(models.Category, pk=pk)
        if user != category.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        form = forms.CategoryForm(instance=category)
        return render(request=request, template_name='transactions/modify_category.html',
                      context={"form": form, "object": category})


class AddCounterpartyView(View):
    def post(self, request):
        form = forms.CounterpartyForm(request.POST)
        if form.is_valid():
            exists = models.Counterparty.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "Counterparty already exists")
            else:
                counterparty = form.save(commit=False)
                counterparty.owner = get_user(request)
                counterparty.save()
                messages.success(request, "Counterparty successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_counterparty')

    def get(self, request):
        form = forms.CounterpartyForm
        return render(request=request, template_name='transactions/add_counterparty.html', context={"form": form})


class ModifyCounterpartyView(View):
    def post(self, request, pk):
        form = forms.CounterpartyForm(request.POST)
        if form.is_valid():
            counterparty = get_object_or_404(models.Counterparty, pk=pk)
            counterparty.name = form.cleaned_data.get("name")
            counterparty.description = form.cleaned_data.get("description")
            counterparty.save()
            messages.success(request, "Counterparty successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_counterparty')

    def get(self, request, pk):
        user = get_user(request)
        counterparty = get_object_or_404(models.Counterparty, pk=pk)
        if user != counterparty.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        form = forms.CounterpartyForm(instance=counterparty)
        return render(request=request, template_name='transactions/modify_counterparty.html',
                      context={"form": form, "object": counterparty})


class AddWalletView(View):
    def post(self, request):
        form = forms.WalletForm(request.POST)
        if form.is_valid():
            exists = models.Wallet.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "Wallet already exists")
            else:
                wallet = form.save(commit=False)
                wallet.owner = get_user(request)
                wallet.save()
                messages.success(request, "Wallet successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_wallet')

    def get(self, request):
        form = forms.WalletForm
        return render(request=request, template_name='transactions/add_wallet.html', context={"form": form})


class ModifyWalletView(View):
    def post(self, request, pk):
        form = forms.WalletForm(request.POST)
        if form.is_valid():
            wallet = get_object_or_404(models.Wallet, pk=pk)
            wallet.name = form.cleaned_data.get("name")
            wallet.description = form.cleaned_data.get("description")
            wallet.save()
            messages.success(request, "Wallet successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_wallet')

    def get(self, request, pk):
        user = get_user(request)
        wallet = get_object_or_404(models.Wallet, pk=pk)
        if user != wallet.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        form = forms.WalletForm(instance=wallet)
        return render(request=request, template_name='transactions/modify_wallet.html',
                      context={"form": form, "object": wallet})


class ListTransactionView(View):
    def get(self, request):
        user = get_user(request)
        if not user:
            return redirect('login')
        transactions = models.Transaction.objects.filter(owner=user).order_by('date')
        return render(request, 'transactions/list_transaction.html', context={"object_list": transactions})


class ListCategoryView(View):
    def get(self, request):
        user = get_user(request)
        if not user:
            return redirect('login')
        categories = models.Category.objects.filter(owner=user).order_by('name')
        return render(request, 'transactions/list_category.html', context={"object_list": categories})


class ListCounterpartyView(View):
    def get(self, request):
        user = get_user(request)
        if not user:
            return redirect('login')
        counterparties = models.Counterparty.objects.filter(owner=user).order_by('name')
        return render(request, 'transactions/list_counterparty.html', context={"object_list": counterparties})


class ListWalletView(View):
    def get(self, request):
        user = get_user(request)
        if not user:
            return redirect('login')
        wallets = models.Wallet.objects.filter(owner=user).order_by('name')
        return render(request, 'transactions/list_wallet.html', context={"object_list": wallets})


class DeleteCounterpartyView(View):
    def get(self, request, pk):
        user = get_user(request)
        counterparty = get_object_or_404(models.Counterparty, pk=pk)
        if user != counterparty.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        counterparty.delete()
        messages.success(request, "Counterparty successfully removed")
        return redirect('transactions:list_counterparty')


class DeleteCategoryView(View):
    def get(self, request, pk):
        user = get_user(request)
        category = get_object_or_404(models.Category, pk=pk)
        if user != category.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        category.delete()
        messages.success(request, "Category successfully removed")
        return redirect('transactions:list_category')


class DeleteTransactionView(View):
    def get(self, request, pk):
        user = get_user(request)
        transaction = get_object_or_404(models.Transaction, pk=pk)
        if user != transaction.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        transaction.delete()
        messages.success(request, "Transaction successfully removed")
        return redirect('transactions:list_transaction')


class DeleteWalletView(View):
    def get(self, request, pk):
        user = get_user(request)
        wallet = get_object_or_404(models.Wallet, pk=pk)
        if user != wallet.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        wallet.delete()
        messages.success(request, "Wallet successfully removed")
        return redirect('transactions:list_wallet')
