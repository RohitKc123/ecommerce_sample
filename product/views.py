from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q, Sum
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import product_form, OrderForm
from django.contrib.auth.decorators import login_required
from .models import Product, WishList, USER, Order
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import requests


# from ..common.constant import IN_STOCK, PROCESSOR


# Create your views here.

@login_required(login_url="/account/login/")
def product_add(request):
    if request.method == 'POST':
        form = product_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, "Product Added Successfully.")
            return redirect('/add/')
        else:
            messages.error(request, "Invalid form")
            return redirect('/add/')
    elif request.method == 'GET':
        form = product_form()
    return render(request, 'add_product.html', {'form': form})


def product_list(request):
    data = Product.objects.filter(featured=True).exclude(quantity=0).order_by("-quantity")
    data1 = Product.objects.all().order_by("-added_date").exclude(quantity=0).exclude(featured=True)
    num = 4
    featured_product_pagination = page_pagination(request, data, num)
    latest_product_pagination = page_pagination(request, data1, num)

    return render(request, 'product_list.html',
                  {'data': featured_product_pagination, 'data1': latest_product_pagination})


@login_required(login_url="/account/login/")
def add_to_wishlist(request):
    if request.method == 'POST':
        quantity = int(request.POST.get('hidden-quantity-field'))
        p_id = request.POST.get('item')
        try:
            product_object = Product.objects.get(id=p_id)
        except ObjectDoesNotExist:
            messages.error(request, "Product with that id does not exist")
            return redirect('/')
        if request.user.id == product_object.user.id:
            messages.error(request, "You cannot buy this product")
            return redirect('/')
        if int(quantity) <= product_object.quantity:
            if not WishList.objects.filter(user=request.user, wished_item=product_object).exclude(
                    Q(status="Canceled") | Q(status="Completed") | Q(status="In Review")).exists():
                wishlist_instance = WishList.objects.create(user=request.user, wished_item=product_object,
                                                            status="Pending")
                wishlist_instance.price = int(quantity) * wishlist_instance.wished_item.price

                wishlist_instance.product_qty = quantity

                wishlist_instance.save()
                product_object.quantity = product_object.quantity - int(quantity)
                product_object.save()
            else:
                try:
                    wishlist_inst = WishList.objects.get(user=request.user, wished_item=product_object,
                                                         status="Pending")
                    old_quantity = wishlist_inst.product_qty
                    old_price = wishlist_inst.price
                    wishlist_inst.product_qty += int(quantity)
                    product_object.quantity -= int(quantity)
                    wishlist_inst.price = int(quantity) * wishlist_inst.wished_item.price + old_price
                    product_object.save()
                    wishlist_inst.save()
                except ObjectDoesNotExist:
                    messages.error(request, "Object does not exist")
                    return redirect("/wishlist/")

        else:
            messages.error(request, "Ordered Quantity cannot be more than Available")
            return redirect('/')
    items = WishList.objects.filter(user=request.user, status="Pending")
    total_price = sum([item.price if (item.status == "Pending") else 0 for item in items])
    form = OrderForm()
    return render(request, 'wish_list.html', {'wishlist_queryset': items, 'total_price': total_price, 'form': form})


def delete_order(request, id, quantity):
    if request.method == 'POST':
        try:
            object = WishList.objects.get(id=id)

        except ObjectDoesNotExist:
            messages.error(request, "Object does not exist")
        object.status = "Canceled"
        object.save()
        if object.status == "Canceled":
            product = object.wished_item
            product.quantity = product.quantity + quantity
            product.save()
    else:
        return render(request, 'wish_list.html')

    return redirect('/wishlist/')


def update_price(request, id):
    if request.method == 'POST':
        quantity = int(request.POST.get('hidden-quantity-field'))
        p_id = request.POST['item']
        wishlist_qty = WishList.objects.get(id=id)
        try:
            item = WishList.objects.get(id=p_id)
            product = item.wished_item
            if int(quantity) <= product.quantity + wishlist_qty.product_qty:
                old_quantity = item.product_qty
                item.product_qty = quantity
                item.price = int(quantity) * product.price
                product.quantity = product.quantity + int(old_quantity) - int(quantity)
                product.save()
                item.save()
            else:
                messages.error(request, "Quantity cannot be more than available")
        except ObjectDoesNotExist:
            messages.error(request, "Object does not exist")

    return redirect('/wishlist/')


def category_filter(request, category):
    filtered_product = Product.objects.filter(category__icontains=category).exclude(quantity=0)
    if len(list(filtered_product)) > 8:
        num = 8
        page = page_pagination(request, filtered_product, num)
    else:
        page = filtered_product
    companies = set(filtered_product.values_list('company', flat=True))

    return render(request, 'filtered.html',
                  {'filtered_product': page, "companies": companies, "category": category, 'flag': True})


def filterby_company(request, category, company):
    product_company = Product.objects.filter(company__icontains=company, category__icontains=category).exclude(
        quantity=0)
    num = 8
    page = page_pagination(request, product_company, num)
    return render(request, 'filtered.html', {'filtered_product': page, "category": category, "company": company})


def filterby_price(request, category, company, price):
    lower = price.split('-')[0]
    upper = price.split('-')[-1]
    product_filterby_price = Product.objects.filter(company__icontains=company, category__icontains=category,
                                                    price__gte=lower, price__lte=upper).exclude(quantity=0)
    page = page_pagination(request, product_filterby_price)

    return render(request, 'filtered.html',
                  {'filtered_product': page, 'flag': True, "category": category, "company": company, 'price': price})


def page_pagination(request, data, num):
    paginator = Paginator(data, num)

    # page_num = request.GET.get('page', 1)
    try:
        page = request.GET.get('page', 1)
    except EmptyPage:
        page = 1
    try:
        pages = paginator.page(page)
    except EmptyPage:
        pages = paginator.page(page)
    return pages


def search_form(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        searched_item = Product.objects.filter(
            Q(name__icontains=query) | Q(company__icontains=query) | Q(category__icontains=query)).exclude(
            quantity=0)
        if searched_item:
            if len(list(searched_item)) > 8:
                num = 8
                page = page_pagination(request, searched_item, num)
            else:
                page = searched_item
        else:

            return render(request, 'productnotfound.html')
            # return redirect('/')

    return render(request, 'searched_product.html', {'data': page})


def email_send(request, id, itemid, quantity, price):
    if request.method == 'POST':
        wishitem = request.POST.get('wisheditem')
        template = render_to_string('email.html', {'name': request.user.first_name})
        email = EmailMessage(
            'Thanks for purchasing',
            template,
            settings.EMAIL_HOST_USER,
            [request.user.email, settings.EMAIL_HOST_USER]
        )
        email.fail_silently = False
        email.send()
        user = USER.objects.get(id=id)
        product = Product.objects.get(id=itemid)
        messages.success(request, "Thanks for purchasing!")
        del_item = WishList.objects.get(id=wishitem)
        del_item.delete()
    else:
        return redirect('/wishlist/')

    return render(request, 'success.html', {'user': user, 'product': product, 'quantity': quantity, 'price': price})


def checkout(request):
    items = WishList.objects.filter(user=request.user, status="Pending")
    total_price = sum([item.price if (item.status == "Pending") else 0 for item in items])
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            pm = form.cleaned_data.get("payment_method")
            user = request.user
            order_by = form.cleaned_data['order_by']
            email = form.cleaned_data['email']
            address = form.cleaned_data['shipping_address']
            mobile = form.cleaned_data['mobile']
            instance = Order.objects.create(user=user, order_by=order_by, email=email,
                                            shipping_address=address, mobile=mobile,
                                            payment_method=pm, total=total_price)
            for item in items:
                instance.ordered_item.add(item)
            instance.save()
            if pm == "Khalti":
                # items.update(status="Completed")
                return redirect(f'/khalti/{instance.id}/')
            else:
                template = render_to_string('email.html', {'name': order_by})
                email = EmailMessage(
                    'Thanks for purchasing',
                    template,
                    settings.EMAIL_HOST_USER,
                    [email, settings.EMAIL_HOST_USER]
                )
                email.fail_silently = False
                email.send()
                items.update(status="Completed")
                messages.success(request, "Thank you for Purchasing!")
                return redirect('/')
        else:
            messages.error(request, "Invalid Phone number")
            return redirect('/wishlist/')
        return redirect('/wishlist/')

    elif request.method == 'GET':
        form = OrderForm()

    return render(request, 'wish_list.html', {'items': items, 'form': form, 'total_price': total_price, "open": True})


def about_page(request):
    return render(request, 'about.html')


def khaltirequest_confirm(request, id, *args, **kwargs):
    order = Order.objects.get(id=id)
    context = {
        "order": order
    }
    return render(request, 'khalti.html', context)


def khalti_verify(request, *args, **kwargs):
    token = request.GET.get("token")
    amount = request.GET.get("amount")
    o_id = request.GET.get("order_id")

    url = "https://khalti.com/api/v2/payment/verify/"

    payload = {
        'token': token,
        'amount': amount
    }

    headers = {
        'Authorization': 'Key test_secret_key_c4b3bff221c94b9782827a38c6432ad8'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    order_obj = Order.objects.get(id=o_id)
    resp_dict = response.json()
    if resp_dict.get("idx"):
        success = True
        order_obj.payment_completed = True
        order_obj.ordered_item.update(status="Completed")
        order_obj.save()

    else:
        success = False
    data = {
        "success": success
    }
    return JsonResponse(data)


def product_description(request, id):
    p_id = Product.objects.get(id=id)
    related_id = Product.objects.filter(category=p_id.category).exclude(Q(id=id) | Q(quantity=0))
    num = 4
    page = page_pagination(request, related_id, num)
    return render(request, 'product_description.html', {'item': p_id, 'related_product': page})


def featured_product_page(request):
    featured_product = Product.objects.filter(featured=True).exclude(quantity=0).order_by("-quantity")
    if len(list(featured_product)) > 8:
        num = 8
        page = page_pagination(request, featured_product, num)
    else:
        page = featured_product
    return render(request, 'featured_product.html', {'featured_product': page})


def latest_product_page(request):
    latest_product = Product.objects.all().exclude(quantity=0).order_by("-added_date").exclude(featured=True)
    if len(list(latest_product)) > 8:
        num = 8
        page = page_pagination(request, latest_product, num)
    else:
        page = latest_product
    return render(request, 'latest_product.html', {'latest_product': page})
