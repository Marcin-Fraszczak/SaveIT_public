from calendar import monthrange
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from . import forms
from .models import Transaction
from categories.models import Category
from counterparties.models import Counterparty
from wallets.models import Wallet


class AddTransactionView(LoginRequiredMixin, View):
    def post(self, request):

        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            wallets = list(form.cleaned_data.get("wallet"))
            transaction = form.save(commit=False)
            transaction.owner = get_user(request)

            if transaction.is_profit:
                transaction.value = abs(transaction.value)
            else:
                transaction.value = -abs(transaction.value)

            transaction.save()
            if wallets:
                transaction.wallet.set(wallets)
                transaction.save()
            messages.success(request, "Transaction successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_transaction')

    def get(self, request):
        user = get_user(request)
        form = forms.TransactionForm()
        form.fields['wallet'].queryset = Wallet.objects.filter(owner=user)
        form.fields['category'].queryset = Category.objects.filter(owner=user)
        form.fields['counterparty'].queryset = Counterparty.objects.filter(owner=user)
        return render(request=request, template_name='transactions/add_transaction.html', context={"form": form})


class ModifyTransactionView(LoginRequiredMixin, View):
    def post(self, request, pk):

        form = forms.TransactionForm(request.POST)
        if form.is_valid():
            transaction = get_object_or_404(Transaction, pk=pk)
            transaction.date = form.cleaned_data.get("date")
            transaction.value = form.cleaned_data.get("value")
            transaction.is_profit = form.cleaned_data.get("is_profit")

            if transaction.is_profit:
                transaction.value = abs(transaction.value)
            else:
                transaction.value = -abs(transaction.value)

            transaction.description = form.cleaned_data.get("notes")
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
        transaction = get_object_or_404(Transaction, pk=pk)

        if user != transaction.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        form = forms.TransactionForm(instance=transaction)
        form.fields['wallet'].queryset = Wallet.objects.filter(owner=user)
        form.fields['category'].queryset = Category.objects.filter(owner=user)
        form.fields['counterparty'].queryset = Counterparty.objects.filter(owner=user)
        return render(request=request, template_name='transactions/modify_transaction.html',
                      context={"form": form, "object": transaction})


last_sort_order_trans = "date"


class ListTransactionView(LoginRequiredMixin, View):

    def get(self, request):

        global last_sort_order_trans

        user = get_user(request)

        word_filter = request.GET.get("wordFilter", "")
        value_filter = request.GET.get("valueFilter", 0)
        raw_sort_order = request.GET.get('order', '-date')
        filter_by = request.GET.get('filter_by', None)
        filter_val = request.GET.get('filter_val')
        from_date = request.GET.get('fromDate', "")
        to_date = request.GET.get('toDate', "")

        if from_date and to_date == '1000-01-01':
            date = from_date.split("-")
            try:
                year = int(date[0])
                month = int(date[1])
            except ValueError as e:
                messages.error(request, "Wrong date input")
                return redirect("accounts:dashboard")
            to_date = datetime(year=year, month=month, day=monthrange(year, month)[1])

        if not from_date:
            from_date = datetime(year=2000, month=1, day=1).date()
        if not to_date:
            to_date = datetime.now().date()

        if raw_sort_order == last_sort_order_trans:
            sort_order = f"-{raw_sort_order.replace('-', '')}"
        else:
            sort_order = raw_sort_order

        last_sort_order_trans = sort_order
        transactions = Transaction.objects.filter(owner=user, date__range=(from_date, to_date))

        if filter_by == 'category':
            transactions = transactions.filter(category=filter_val).order_by(sort_order)
        elif filter_by == 'counterparty':
            transactions = transactions.filter(counterparty=filter_val).order_by(sort_order)
        elif filter_by == 'wallet':
            transactions = transactions.filter(wallet=filter_val).order_by(sort_order)

        if raw_sort_order in ["category", "counterparty", "wallet"]:
            transactions = transactions.order_by(f"{sort_order}__name")
        else:
            transactions = transactions.order_by(sort_order)

        return render(request, 'transactions/list_transaction.html',
                      context={
                          "object_list": transactions,
                          "word_filter": word_filter,
                          "value_filter": value_filter,
                          "filter_by": filter_by,
                          "filter_val": filter_val,
                          "from_date": from_date,
                          "to_date": to_date,
                      })


class DeleteTransactionView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_user(request)

        transaction = get_object_or_404(Transaction, pk=pk)

        if user != transaction.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        transaction.delete()
        messages.success(request, "Transaction successfully removed")
        return redirect('transactions:list_transaction')
