from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import forms

from transactions.models import Transaction
from .models import Wallet


class AddWalletView(LoginRequiredMixin, View):
    def post(self, request):

        form = forms.WalletForm(request.POST)
        if form.is_valid():
            wallet = form.save(commit=False)
            wallet.owner = get_user(request)
            wallet.name = wallet.name.upper()
            wallet.unique_name = f"{get_user(request).username}_{wallet.name}"

            exists = Wallet.objects.filter(unique_name=wallet.unique_name)

            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
                wallet.save()
                messages.success(request, "Wallet successfully added")
        else:
            messages.error(request, "Error saving form")

        return redirect('wallets:list_wallet')

    def get(self, request):

        form = forms.WalletForm
        return render(request=request, template_name='transactions/add_wallet.html', context={"form": form})


class ModifyWalletView(LoginRequiredMixin, View):
    def post(self, request, pk):

        if 'delete' in request.POST:
            user = get_user(request)

            wallet = get_object_or_404(Wallet, pk=pk)

            if user != wallet.owner:
                messages.error(request, "Access denied")
                return redirect('login')

            wallet.delete()
            messages.success(request, "Wallet successfully removed")
            return redirect('wallets:list_wallet')


        form = forms.WalletForm(request.POST)
        if form.is_valid():
            wallet = get_object_or_404(Wallet, pk=pk)
            wallet.name = form.cleaned_data.get("name").upper()
            wallet.unique_name = f"{get_user(request).username}_{wallet.name}"
            wallet.description = form.cleaned_data.get("description")

            exists = Wallet.objects.filter(unique_name=wallet.unique_name).exclude(pk=pk)

            if exists:
                messages.error(request, "This name already exists")
                return redirect(request.get_full_path())
            else:
                wallet.save()
                messages.success(request, "Wallet successfully modified")

        else:
            messages.error(request, "Error saving form")

        return redirect('wallets:list_wallet')

    def get(self, request, pk):

        user = get_user(request)
        wallet = get_object_or_404(Wallet, pk=pk)

        if user != wallet.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        form = forms.WalletForm(instance=wallet)
        return render(request=request, template_name='transactions/modify_wallet.html',
                      context={"form": form, "object": wallet})


last_sort_order_wallet = '-name'


class ListWalletView(LoginRequiredMixin, View):
    def get(self, request):

        global last_sort_order_wallet

        user = get_user(request)

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_wallet:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_wallet = sort_order

        wallets = Wallet.objects.filter(owner=user).order_by(sort_order)
        default_wallet = wallets.filter(is_default=True)
        if not len(default_wallet):
            default_wallet.pk = 0

        return render(request, 'transactions/list_wallet.html',
                      context={
                          "object_list": wallets,
                          "word_filter": word_filter,
                          "default_wallet": default_wallet,
                      })

#
# class DeleteWalletView(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         user = get_user(request)
#
#         wallet = get_object_or_404(Wallet, pk=pk)
#
#         if user != wallet.owner:
#             messages.error(request, "Access denied")
#             return redirect('login')
#
#         wallet.delete()
#         messages.success(request, "Wallet successfully removed")
#         return redirect('wallets:list_wallet')


class TransferWalletView(LoginRequiredMixin, View):
    def get(self, request, from_pk, to_pk):

        user = get_user(request)

        from_wallet = get_object_or_404(Wallet, pk=from_pk)
        transactions = Transaction.objects.filter(wallet=from_wallet)

        if to_pk == 0:
            other_wallets = Wallet.objects.filter(owner=user).exclude(pk=from_pk)
            return render(request, 'transactions/transfer_wallet.html',
                          context={
                              "from_wallet": from_wallet,
                              "object_list": other_wallets,
                              "transactions": transactions,
                          })

        else:
            to_wallet = get_object_or_404(Wallet, owner=user, pk=to_pk)
            for transaction in transactions:
                transaction.wallet.remove(from_wallet)
                transaction.wallet.add(to_wallet)
                transaction.save()

            messages.success(request,
                             f"{len(transactions)} transactions successfully transferred from {from_wallet.name} to {to_wallet.name}")
            return redirect('wallets:list_wallet')


class MakeDefaultWalletView(LoginRequiredMixin, View):
    def get(self, request, from_pk, to_pk):

        user = get_user(request)

        if from_pk == 0:
            to_wallet = Wallet.objects.get(pk=to_pk)
            if to_wallet.owner != user:
                messages.error(request, "Access denied")
                return redirect('wallets:list_wallet')
        else:
            to_wallet = Wallet.objects.get(pk=to_pk)
            from_wallet = Wallet.objects.get(pk=from_pk)
            if from_wallet.owner != user or to_wallet.owner != user:
                messages.error(request, "Access denied")
                return redirect('wallets:list_wallet')

        all_wallets = Wallet.objects.filter(owner=user)

        for wallet in all_wallets:
            if wallet.pk == to_pk:
                wallet.is_default = 1
                wallet.save()
            else:
                wallet.is_default = 0
                wallet.save()

        messages.success(request, "Default wallet changed successfully")
        return redirect('wallets:list_wallet')
