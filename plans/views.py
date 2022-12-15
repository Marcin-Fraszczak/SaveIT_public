from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import SavingsPlan
from . import forms


class AddSavingsPlanView(LoginRequiredMixin, View):
    def post(self, request):

        form = forms.SavingsPlanForm(request.POST)
        if form.is_valid():
            savings_plan = form.save(commit=False)
            savings_plan.owner = get_user(request)
            savings_plan.name = savings_plan.name.upper()
            savings_plan.unique_name = f"{get_user(request).username}_{savings_plan.name}"

            exists = SavingsPlan.objects.filter(unique_name=savings_plan.unique_name)

            if exists:
                messages.error(request, "This name already exists")
            else:
                savings_plan.save()
                messages.success(request, "Savings plan successfully added")

        else:
            messages.error(request, "Error saving form")

        return redirect('plans:list_savings_plan')

    def get(self, request):

        form = forms.SavingsPlanForm
        return render(request=request, template_name='transactions/add_savings_plan.html', context={"form": form})


class ModifySavingsPlanView(LoginRequiredMixin, View):
    def post(self, request, pk):

        if 'delete' in request.POST:
            user = get_user(request)

            savings_plan = get_object_or_404(SavingsPlan, pk=pk)

            if user != savings_plan.owner:
                messages.error(request, "Access denied")
                return redirect('login')

            savings_plan.delete()
            messages.success(request, "Savings plan successfully removed")
            return redirect('plans:list_savings_plan')

        form = forms.SavingsPlanForm(request.POST)
        if form.is_valid():
            savings_plan = get_object_or_404(SavingsPlan, pk=pk)
            savings_plan.name = form.cleaned_data.get("name").upper()
            savings_plan.unique_name = f"{get_user(request).username}_{savings_plan.name}"
            savings_plan.monthly_goal = form.cleaned_data.get("monthly_goal")
            savings_plan.initial_value = form.cleaned_data.get("initial_value")
            savings_plan.curve_type = form.cleaned_data.get("curve_type")

            exists = SavingsPlan.objects.filter(unique_name=savings_plan.unique_name).exclude(pk=pk)

            if exists:
                messages.error(request, "This name already exists")
            else:
                savings_plan.save()
                messages.success(request, "Savings plan successfully added")

        else:
            messages.error(request, "Error saving form")

        return redirect('plans:list_savings_plan')

    def get(self, request, pk):

        user = get_user(request)
        savings_plan = get_object_or_404(SavingsPlan, pk=pk)

        if user != savings_plan.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        form = forms.SavingsPlanForm(instance=savings_plan)
        return render(request=request, template_name='transactions/modify_savings_plan.html',
                      context={"form": form, "object": savings_plan})


last_sort_order_plan = '-name'


class ListSavingsPlanView(LoginRequiredMixin, View):
    def get(self, request):
        global last_sort_order_plan

        user = get_user(request)

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_plan:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_plan = sort_order

        plans = SavingsPlan.objects.filter(owner=user).order_by(sort_order)
        return render(request, 'transactions/list_savings_plan.html',
                      context={
                          "object_list": plans,
                          "word_filter": word_filter,
                      })


#
# class DeleteSavingsPlanView(LoginRequiredMixin, View):
#     def get(self, request, pk):
#         user = get_user(request)
#
#         savings_plan = get_object_or_404(SavingsPlan, pk=pk)
#
#         if user != savings_plan.owner:
#             messages.error(request, "Access denied")
#             return redirect('login')
#
#         savings_plan.delete()
#         messages.success(request, "Savings plan successfully removed")
#         return redirect('plans:list_savings_plan')


class MakeDefaultPlanView(LoginRequiredMixin, View):
    def get(self, request, pk):

        user = get_user(request)
        default_plan = SavingsPlan.objects.get(pk=pk)
        if default_plan.owner != user:
            messages.error(request, "Access denied")
            return redirect('plans:list_savings_plan')

        all_plans = SavingsPlan.objects.filter(owner=user)

        for plan in all_plans:
            if plan.pk == pk:
                plan.is_default = 1
                plan.save()
            else:
                plan.is_default = 0
                plan.save()

        messages.success(request, "Default Savings plan changed successfully")
        return redirect('plans:list_savings_plan')
