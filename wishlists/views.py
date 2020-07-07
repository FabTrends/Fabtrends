from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from cart.forms import CartAddProductForm
from fabtrendapp.models import Product
from wishlists.models import WishList
from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from cart.forms import CartAddProductForm
from fabtrendapp.forms import feedbackform, queryform, Productform
from fabtrendapp.models import contact, category, FAQs, Product, subcategory, feedback



def add_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_id = request.user.id

    wl = WishList(user_id=user_id, product=product)
    wl.save()
    if wl:
        messages.success(request, 'WishLists Created SuccessFully')
        return redirect('/')
    else:
        messages.warning(request, 'SomeThing Went Wrong')
        return redirect('/')


def my_wishlists(request):
    products = WishList.objects.filter(user_id=request.user.id).select_related('product')
   
    wishlists = []
    
    for i in products:
        i = str(i)
        product = Product.objects.get(pk=i)
        wishlists.append(product)
    cart_product_form = CartAddProductForm()
    context = {
        'title': 'My WishList',
        'wishlists': wishlists,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'wishlists.html', context)


def clear_wishlists(request):
    products = WishList.objects.filter(user_id=request.user.id).select_related('product').delete()
    context = {
        'title': 'My WishList',
    }
    return render(request, 'wishlists.html', context)


def delete_wishlist(request, product_id):
    wl = WishList.objects.get(product=product_id)
    wl.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    