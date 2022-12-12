from calendar import monthrange
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
        if not user.is_authenticated:
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

        for key, value in [("abs_month", abs_month), ("abs_year", abs_year), ("cum_month", cum_month),
                           ("cum_year", cum_year)]:
            graph_data[key] = value

        any_wallet = models.Wallet.objects.filter(owner=user)
        if not any_wallet:
            default_wallet = models.Wallet(
                name="DEFAULT WALLET",
                unique_name=f"{user.username}_DEFAULT WALLET",
                description="Generic wallet to start",
                is_default=1,
                owner=user,
            )
            default_wallet.save()

        any_category = models.Category.objects.filter(owner=user)
        if not any_category:
            default_category = models.Category(
                name="DEFAULT CATEGORY",
                unique_name=f"{user.username}_DEFAULT CATEGORY",
                description="Generic category to start",
                owner=user,
            )
            default_category.save()

        any_counterparty = models.Counterparty.objects.filter(owner=user)
        if not any_counterparty:
            default_counterparty = models.Counterparty(
                name="DEFAULT COUNTERPARTY",
                unique_name=f"{user.username}_DEFAULT COUNTERPARTY",
                description="Generic counterparty to start",
                owner=user,
            )
            default_counterparty.save()

        default_wallet = models.Wallet.objects.filter(owner=user, is_default=True)

        if default_wallet:
            default_wallet = default_wallet[0]

        default_plan = models.SavingsPlan.objects.filter(owner=user, is_default=1)

        if default_plan:
            default_plan = default_plan[0]
            init = default_plan.initial_value
            goal = default_plan.monthly_goal
            diff = goal - init

        def get_data_for_graph(year, month):
            last_day = monthrange(year, month)[1]
            displayed_date = f"{year} / {month}"
            from_date = datetime(year=year, month=month, day=1).date()
            to_date = datetime(year=year, month=month, day=last_day).date()

            if default_wallet:
                transactions = models.Transaction.objects.filter(owner=user, wallet=default_wallet,
                                                                 date__range=(from_date, to_date))
            else:
                transactions = models.Transaction.objects.filter(owner=user, date__range=(from_date, to_date))

            values_list = [[i, 0, 0, 0, 0, 0] for i in range(last_day + 1)]

            if default_plan:
                if default_plan.curve_type != 1:
                    if default_plan.curve_type == 2:
                        medi = init + (diff / 3)
                    else:
                        medi = init + (2 * diff / 3)

                    middle_day = last_day // 2
                    a = ((middle_day - 1) * (goal - init) - (last_day - 1) * (medi - init)) / (
                            (middle_day - 1) * (last_day - 1) * (last_day - middle_day))
                    b = (medi - init) / (middle_day - 1) - a * (middle_day + 1)
                    c = init - b - a

            for tran in transactions:
                val = tran.value
                if tran.is_profit:
                    values_list[tran.date.day][1] += val
                else:
                    values_list[tran.date.day][2] += val

            for i in range(len(values_list)):
                if i == 0:
                    values_list[i][3] = values_list[i][1]
                    values_list[i][4] = values_list[i][2]
                elif i == 1:
                    values_list[i][3] = values_list[i][1] + values_list[i - 1][3]
                    values_list[i][4] = values_list[i][2] + values_list[i - 1][4]
                    if default_plan:
                        values_list[i][5] = init
                else:
                    values_list[i][3] = values_list[i][1] + values_list[i - 1][3]
                    values_list[i][4] = values_list[i][2] + values_list[i - 1][4]
                    if default_plan:
                        if default_plan.curve_type == 1:
                            values_list[i][5] = round(init + diff * (i - 1) / (last_day - 1), 2)
                        elif default_plan.curve_type in [2, 3]:
                            values_list[i][5] = round(a * i * i + b * i + c, 2)

            return displayed_date, values_list[1:], len(transactions)

        abs_displayed_date, abs_values_list, abs_no_transactions = get_data_for_graph(abs_year, abs_month)
        cum_displayed_date, cum_values_list, cum_no_transactions = get_data_for_graph(cum_year, cum_month)

        if default_wallet:
            total_transactions = models.Transaction.objects.filter(owner=user, wallet=default_wallet)
        else:
            total_transactions = models.Transaction.objects.filter(owner=user)

        total_profit = 0
        total_debit = 0

        for trans in total_transactions:
            value = trans.value
            if trans.is_profit:
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
            "total_profit": total_profit,
            "total_debit": total_debit,
            "total_balance": total_debit + total_profit,
            "default_wallet": default_wallet,
            "default_plan": default_plan,
        })
