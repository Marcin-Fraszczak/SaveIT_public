from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from . import models
from . import forms


class AddCounterpartyView(LoginRequiredMixin, View):
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


class ModifyCounterpartyView(LoginRequiredMixin, View):
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


last_sort_order_counterparty = "-name"


class ListCounterpartyView(LoginRequiredMixin, View):
    def get(self, request):
        global last_sort_order_counterparty

        user = get_user(request)

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


class DeleteCounterpartyView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_user(request)

        counterparty = get_object_or_404(models.Counterparty, pk=pk)

        if user != counterparty.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        counterparty.delete()
        messages.success(request, "Counterparty successfully removed")
        return redirect('transactions:list_counterparty')
