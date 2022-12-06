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
            form.save()
            messages.success(request, "Category successfully added")
        else:
            messages.error(request, "Error saving form")
        return redirect('transactions:list_category')

    def get(self, request):

        form = forms.CategoryForm
        return render(request=request, template_name='add_category.html', context={"form": form})


class ListCategoryView(ListView):
    model = models.Category
    template_name = 'list_category.html'
#
#
# class AddCounterpartyView(CreateView):
#     model = models.Counterparty
#     template_name = 'add_counterparty.html'
#     success_url = reverse_lazy('accounts:dashboard')
#     fields = ["name", "description"]
#
#
# class ListCounterpartyView(ListView):
#     model = models.Counterparty
#     template_name = 'list_counterparty.html'
#
#
# class AddWalletView(CreateView):
#     user = get_user_model()
#     model = models.Wallet
#     template_name = 'add_wallet.html'
#     success_url = reverse_lazy('accounts:dashboard')
#     fields = ["name", "description"]
#
#
# class ListWalletView(ListView):
#     model = models.Wallet
#     template_name = 'list_wallet.html'
#
#
#
#
# class AddObjectView(View):
#     objects_dict = {
#         "transaction": models.Transaction,
#         "category": models.Category,
#         "counterparty": models.Counterparty,
#         "wallet": models.Wallet,
#         "savings_plan": models.SavingsPlan,
#     }
#     forms_dict = {
#         # "transaction": forms.TransactionForm,
#         "category": forms.CategoryForm,
#         # "counterparty": forms.CounterpartyForm,
#         # "wallet": forms.WalletForm,
#         # "savings_plan": forms.SavingsPlanForm,
#     }
#
#     def get(self, request, item):
#
#         model = AddObjectView.objects_dict.get(item, None)
#
#         if not model:
#             return redirect('home:home')
#         else:
#             form = AddObjectView.forms_dict.get(item, None)
#             return render(request, 'add_category.html', context={"form": form})




# class AddCategoryView(CreateView):
#     model = models.Category
#     template_name = 'add_category.html'
#     success_url = reverse_lazy('accounts:dashboard')
#     fields = ["name", "description"]
#
#