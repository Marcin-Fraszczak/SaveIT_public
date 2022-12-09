from django.contrib import messages
from django.contrib.auth import get_user
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models
from . import forms


class AddTransactionView(View):
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
            if transaction.is_profit:
                transaction.value = abs(transaction.value)
            else:
                transaction.value = -abs(transaction.value)
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
            category = form.save(commit=False)
            category.owner = get_user(request)
            category.name = category.name.upper()
            category.unique_name = f"{get_user(request).username}_{category.name}"

            exists = models.Category.objects.filter(unique_name=category.unique_name)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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
            category.name = form.cleaned_data.get("name").upper()
            category.unique_name = f"{get_user(request).username}_{category.name}"
            category.description = form.cleaned_data.get("description")

            exists = models.Category.objects.filter(unique_name=category.unique_name).exclude(pk=pk)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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
            counterparty = form.save(commit=False)
            counterparty.owner = get_user(request)
            counterparty.name = counterparty.name.upper()
            counterparty.unique_name = f"{get_user(request).username}_{counterparty.name}"

            exists = models.Counterparty.objects.filter(unique_name=counterparty.unique_name)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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
            counterparty.name = form.cleaned_data.get("name").upper()
            counterparty.unique_name = f"{get_user(request).username}_{counterparty.name}"
            counterparty.description = form.cleaned_data.get("description")

            exists = models.Category.objects.filter(unique_name=counterparty.unique_name).exclude(pk=pk)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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
            wallet = form.save(commit=False)
            wallet.owner = get_user(request)
            wallet.name = wallet.name.upper()
            wallet.unique_name = f"{get_user(request).username}_{wallet.name}"

            exists = models.Wallet.objects.filter(unique_name=wallet.unique_name)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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
            wallet.name = form.cleaned_data.get("name").upper()
            wallet.unique_name = f"{get_user(request).username}_{wallet.name}"
            wallet.description = form.cleaned_data.get("description")

            exists = models.Wallet.objects.filter(unique_name=wallet.unique_name).exclude(pk=pk)
            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
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


last_sort_order_trans = "date"


class ListTransactionView(View):

    def get(self, request):
        global last_sort_order_trans

        user = get_user(request)

        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        word_filter = request.GET.get("wordFilter", "")
        value_filter = request.GET.get("valueFilter", 0)
        sort_order = request.GET.get('order', '-date')
        filter_by = request.GET.get('filter_by', None)
        filter_val = request.GET.get('filter_val')

        if sort_order == last_sort_order_trans:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_trans = sort_order

        if filter_by == 'category':
            transactions = models.Transaction.objects.filter(owner=user, category=filter_val).order_by(sort_order)
        elif filter_by == 'counterparty':
            transactions = models.Transaction.objects.filter(owner=user, counterparty=filter_val).order_by(sort_order)
        elif filter_by == 'wallet':
            transactions = models.Transaction.objects.filter(owner=user, wallet=filter_val).order_by(sort_order)
        else:
            transactions = models.Transaction.objects.filter(owner=user).order_by(sort_order)

        return render(request, 'transactions/list_transaction.html',
                      context={
                          "object_list": transactions,
                          "word_filter": word_filter,
                          "value_filter": value_filter,
                          "filter_by": filter_by,
                          "filter_val": filter_val,
                      })


last_sort_order_category = "-name"


class ListCategoryView(View):
    def get(self, request):
        global last_sort_order_category
        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_category:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_category = sort_order

        categories = models.Category.objects.filter(owner=user).order_by(sort_order)
        return render(request, 'transactions/list_category.html',
                      context={
                          "object_list": categories,
                          "word_filter": word_filter,
                      })


last_sort_order_counterparty = "-name"


class ListCounterpartyView(View):
    def get(self, request):
        global last_sort_order_counterparty
        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_counterparty:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_counterparty = sort_order

        counterparties = models.Counterparty.objects.filter(owner=user).order_by(sort_order)
        return render(request, 'transactions/list_counterparty.html',
                      context={
                          "object_list": counterparties,
                          "word_filter": word_filter,
                      })


last_sort_order_wallet = '-name'


class ListWalletView(View):
    def get(self, request):
        global last_sort_order_wallet
        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_wallet:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_wallet = sort_order

        wallets = models.Wallet.objects.filter(owner=user).order_by(sort_order)
        return render(request, 'transactions/list_wallet.html',
                      context={
                          "object_list": wallets,
                          "word_filter": word_filter,
                      })


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


class AddSavingsPlanView(View):
    def post(self, request):
        form = forms.SavingsPlanForm(request.POST)
        if form.is_valid():
            exists = models.SavingsPlan.objects.filter(name=request.POST.get('name'))
            if exists:
                messages.error(request, "This name already exists")
            else:
                savings_plan = form.save(commit=False)
                savings_plan.owner = get_user(request)
                savings_plan.save()
                messages.success(request, "Savings plan successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_savings_plan')

    def get(self, request):
        form = forms.SavingsPlanForm
        return render(request=request, template_name='transactions/add_savings_plan.html', context={"form": form})


class DeleteSavingsPlanView(View):
    def get(self, request, pk):
        user = get_user(request)
        savings_plan = get_object_or_404(models.SavingsPlan, pk=pk)
        if user != savings_plan.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        savings_plan.delete()
        messages.success(request, "Savings plan successfully removed")
        return redirect('transactions:list_savings_plan')


class ModifySavingsPlanView(View):
    def post(self, request, pk):
        form = forms.SavingsPlanForm(request.POST)
        if form.is_valid():
            savings_plan = get_object_or_404(models.SavingsPlan, pk=pk)
            savings_plan.name = form.cleaned_data.get("name")
            savings_plan.monthly_goal = form.cleaned_data.get("monthly_goal")
            savings_plan.initial_value = form.cleaned_data.get("initial_value")
            savings_plan.curve_type = form.cleaned_data.get("curve_type")
            savings_plan.save()
            messages.success(request, "Savings plan successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('transactions:list_savings_plan')

    def get(self, request, pk):
        user = get_user(request)
        savings_plan = get_object_or_404(models.SavingsPlan, pk=pk)
        if user != savings_plan.owner:
            messages.error(request, "Access denied")
            return redirect('login')
        form = forms.SavingsPlanForm(instance=savings_plan)
        return render(request=request, template_name='transactions/modify_savings_plan.html',
                      context={"form": form, "object": savings_plan})


class ListSavingsPlanView(View):
    def get(self, request):
        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')
        savings_plan = models.SavingsPlan.objects.filter(owner=user).order_by('name')
        return render(request, 'transactions/list_savings_plan.html', context={"object_list": savings_plan})


class TransferWalletView(View):
    def get(self, request, from_pk, to_pk):
        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        from_wallet = get_object_or_404(models.Wallet, pk=from_pk)
        transactions = models.Transaction.objects.filter(wallet=from_wallet)

        if to_pk == 0:
            other_wallets = models.Wallet.objects.filter(owner=user).exclude(pk=from_pk)
            return render(request, 'transactions/transfer_wallet.html',
                          context={
                              "from_wallet": from_wallet,
                              "object_list": other_wallets,
                              "transactions": transactions,
                          })
        else:
            to_wallet = get_object_or_404(models.Wallet, owner=user, pk=to_pk)
            for transaction in transactions:
                transaction.wallet.remove(from_wallet)
                transaction.wallet.add(to_wallet)
                transaction.save()
            messages.success(request, f"{len(transactions)} transactions successfully transferred from {from_wallet.name} to {to_wallet.name}")
            return redirect('transactions:list_wallet')
