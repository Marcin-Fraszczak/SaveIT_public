from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Category
from . import forms


class AddCategoryView(LoginRequiredMixin, View):
    def post(self, request):

        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = get_user(request)
            category.name = category.name.upper()
            category.unique_name = f"{get_user(request).username}_{category.name}"

            exists = Category.objects.filter(unique_name=category.unique_name)

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


class ModifyCategoryView(LoginRequiredMixin, View):
    def post(self, request, pk):

        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            category = get_object_or_404(Category, pk=pk)
            category.name = form.cleaned_data.get("name").upper()
            category.unique_name = f"{get_user(request).username}_{category.name}"
            category.description = form.cleaned_data.get("description")

            exists = Category.objects.filter(unique_name=category.unique_name).exclude(pk=pk)
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
        category = get_object_or_404(Category, pk=pk)

        if user != category.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        form = forms.CategoryForm(instance=category)
        return render(request=request, template_name='transactions/modify_category.html',
                      context={"form": form, "object": category})


last_sort_order_category = "-name"


class ListCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        global last_sort_order_category

        user = get_user(request)

        word_filter = request.GET.get("wordFilter", "")
        sort_order = request.GET.get('order', 'name')

        if sort_order == last_sort_order_category:
            sort_order = f"-{sort_order.replace('-', '')}"
        last_sort_order_category = sort_order

        categories = Category.objects.filter(owner=user).order_by(sort_order)
        return render(request, 'transactions/list_category.html',
                      context={
                          "object_list": categories,
                          "word_filter": word_filter,
                      })


class DeleteCategoryView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_user(request)

        category = get_object_or_404(Category, pk=pk)

        if user != category.owner:
            messages.error(request, "Access denied")
            return redirect('login')

        category.delete()
        messages.success(request, "Category successfully removed")
        return redirect('transactions:list_category')
