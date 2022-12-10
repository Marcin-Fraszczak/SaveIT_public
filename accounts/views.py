from calendar import monthrange
from collections import defaultdict
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import get_user
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from transactions import models
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/register.html'


graph_data = {
    "abs_month": datetime.today().month,
    "cum_month": datetime.today().month,
    "abs_year": datetime.today().year,
    "cum_year": datetime.today().year,
}


class DashboardView(View):
    def get(self, request):

        user = get_user(request)
        if not user:
            messages.error(request, "You must log in to see this data.")
            return redirect('login')

        abs_month = request.GET.get("abs_month", graph_data.get("abs_month"))
        abs_year = request.GET.get("abs_year", graph_data.get("abs_year"))
        cum_month = request.GET.get("cum_month", graph_data.get("cum_month"))
        cum_year = request.GET.get("cum_year", graph_data.get("cum_year"))
        chain_graphs = request.GET.get("chain_graphs", 1)

        try:
            abs_month = int(abs_month)
            abs_year = int(abs_year)
            cum_month = int(cum_month)
            cum_year = int(cum_year)
            chain_graphs = int(chain_graphs)
        except ValueError as e:
            messages.error(request, "Wrong input")
            return redirect('accounts:dashboard')

        if abs_month > 12:
            abs_month = 1
            abs_year += 1
        elif abs_month < 1:
            abs_month = 12
            abs_year -= 1

        if cum_month > 12:
            cum_month = 1
            cum_year += 1
        elif cum_month < 1:
            cum_month = 12
            cum_year -= 1

        if chain_graphs not in [0, 1]:
            messages.error(request, "Wrong input")
            return redirect('accounts:dashboard')

        if chain_graphs == 1:
            if abs_month == graph_data.get("abs_month") and cum_month != graph_data.get("cum_month"):
                abs_month = cum_month
                abs_year = cum_year
            else:
                cum_month = abs_month
                cum_year = abs_year

        for key, value in [("abs_month", abs_month), ("abs_year", abs_year), ("cum_month", cum_month), ("cum_year", cum_year)]:
            graph_data[key] = value

        def get_data_for_graph(year, month):
            last_day = monthrange(year, month)[1]
            displayed_date = f"{year} / {month}"
            from_date = datetime(year=year, month=month, day=1).date()
            to_date = datetime(year=year, month=month, day=last_day).date()

            transactions = models.Transaction.objects.filter(owner=user, date__range=(from_date, to_date))
            values_list = [[i, 0, 0, 0, 0] for i in range(1, last_day + 1)]

            for transaction in transactions:
                val = transaction.value
                if transaction.is_profit:
                    values_list[transaction.date.day][1] += val
                else:
                    values_list[transaction.date.day][2] += val

            for i in range(len(values_list)):
                if i == 0:
                    values_list[i][3] = values_list[i][1]
                    values_list[i][4] = values_list[i][2]
                values_list[i][3] = values_list[i][1] + values_list[i - 1][3]
                values_list[i][4] = values_list[i][2] + values_list[i - 1][4]

            return displayed_date, values_list, len(transactions)

        abs_displayed_date, abs_values_list, abs_no_transactions = get_data_for_graph(abs_year, abs_month)
        cum_displayed_date, cum_values_list, cum_no_transactions = get_data_for_graph(cum_year, cum_month)

        total_categories = models.Category.objects.filter(owner=user)
        total_counterparties = models.Counterparty.objects.filter(owner=user)
        total_transactions = models.Transaction.objects.filter(owner=user)
        total_profit = 0
        total_debit = 0

        for transaction in total_transactions:
            value = transaction.value
            if transaction.is_profit:
                total_profit += value
            else:
                total_debit += value

        return render(request, "accounts/dashboard.html", context={
            "abs_displayed_date": abs_displayed_date,
            "cum_displayed_date": cum_displayed_date,
            "abs_values_list": abs_values_list,
            "cum_values_list": cum_values_list,
            "abs_year": abs_year,
            "cum_year": cum_year,
            "abs_month": abs_month,
            "cum_month": cum_month,
            "chain_graphs": chain_graphs,
            "abs_no_transactions": abs_no_transactions,
            "cum_no_transactions": cum_no_transactions,
            "monthly_profit": abs_values_list[-1][3],
            "monthly_debit": abs_values_list[-1][4],
            "monthly_balance": abs_values_list[-1][4] + abs_values_list[-1][3],
            "total_transactions": len(total_transactions),
            "total_categories": len(total_categories),
            "total_counterparties": len(total_counterparties),
            "total_profit": total_profit,
            "total_debit": total_debit,
            "total_balance": total_debit + total_profit,
        })
