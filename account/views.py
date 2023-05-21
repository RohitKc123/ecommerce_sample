from django.contrib import messages
from django.shortcuts import render, redirect
from django import forms
from .forms import User_register, LoginForm, UpdateUser
from django.contrib.auth import authenticate, login, logout
from .models import User
from product.models import Order
from django.http import HttpResponse
from django import forms

from product.models import WishList


# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = User_register(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'user_form.html', {'form': form})
        return redirect('/account/login/')

    elif request.method == 'GET':
        form = User_register()
    return render(request, 'user_form.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])

            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'user_login.html', {'form': form})
            return redirect('/account/login/')
        else:
            return render(request, 'user_login.html', {'form': form})

    elif request.method == 'GET':
        if request.user.is_authenticated and not request.user.is_superuser:
            return redirect('account/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'user_login.html', {'form': form})


def dash_board(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        user_product = Order.objects.filter(user=request.user).order_by('created_at')
        if user_product:
            wishlist_items_ids = user_product.values_list('ordered_item', flat=True)
            if WishList.objects.filter(id__in=wishlist_items_ids, status='Completed').exists():
                wishlist_items_queryset = list(WishList.objects.filter(id__in=wishlist_items_ids, status='Completed'))[-1]

                data = User.objects.all()

                return render(request, 'user_dashboard.html',
                            {'data': data, 'wishlist_items_queryset': wishlist_items_queryset,
                                'user_product': user_product})
            else:
                return render(request, 'user_dashboard.html')
        else:
            return render(request, 'user_dashboard.html')

    else:
        return redirect('/account/login/')


def logout_view(request):
    logout(request)
    return redirect('/account/login/')


def edit_profile(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateUser(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/account/dashboard/')
        else:
            return render(request, 'edit_profile.html', {'form': form})
    form = UpdateUser(instance=user)

    return render(request, 'edit_profile.html', {'form': form})


def user_order_history(request):
    user_product = Order.objects.filter(user=request.user).order_by('created_at')
    wishlist_items_ids = user_product.values_list('ordered_item', flat=True)
    wishlist_items_queryset=None
    if WishList.objects.filter(id__in=wishlist_items_ids, status='Completed').exists():
        wishlist_items_queryset = WishList.objects.filter(id__in=wishlist_items_ids, status='Completed').order_by('-added_date')
    # order_product = user_product.ordered_item.exclude(status="pending").exclude(status="In Review").exclude(
    #     status="Canceled").order_by("created_at")
    return render(request, 'user_order_history.html', {'wishlist_items_queryset': wishlist_items_queryset})
