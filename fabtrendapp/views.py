from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, View
from django.core.paginator import Paginator
from cart.forms import CartAddProductForm
from fabtrendapp.forms import feedbackform, queryform, Productform
from fabtrendapp.models import contact, category, FAQs, Product, subcategory, feedback
from .forms import SignUpForm, EditProfileForm,  contactform
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import HttpResponse


class indexpageView(TemplateView):
    template_name = "index.html"


class basepageView(TemplateView):
    template_name = "base.html"


class contactpageView(TemplateView):
    template_name = "contact.html"


class checkoutpageView(TemplateView):
    template_name = "checkout.html"


class belliespageView(TemplateView):
    template_name = "bellies.html"


class privacypageView(TemplateView):
    template_name = "privacy.html"


class aboutpageView(TemplateView):
    template_name = "about.html"


class editView(TemplateView):
    template_name = "edit.html"


class productpageView(TemplateView):
    template_name = "product.html"


class addproductpageview(TemplateView):
    template_name = "addproduct.html"


class basepageView(TemplateView):
    template_name = "base.html"


class FAQspageView(ListView):
    template_name = "FAQs.html"

    def get_queryset(self):
        return FAQs.objects.all()


class querypageview(TemplateView):
    template_name = "query.html"


class listView(ListView):
    template_name = "list.html"

    def get_queryset(self):
        return contact.objects.all()


class Feedbackpageview(TemplateView):
    template_name = "feedback.html"




def post(self, request, text):
    form = contactform(request.POST)
    if form.is_valid():
        form.save()
        text = form.cleaned_data['name']
        text = form.cleaned_data['phoneno']
        text = form.cleaned_data['email']
        text = form.cleaned_data['address']
        form = contactform()
        messages.add_message(request, messages.INFO, 'Submitted.')
        return redirect('/contact')
    args = {'form': form, 'text': text}
    return render(request, self.template_name, args)


def insert(request):
    if request.method == "GET":
        form = contactForm()
    else:
        form = contactform(request.POST, request.FILES)
        name = request.POST.get('name')
        phoneno = request.POST.get('phoneno')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if form.is_valid():
            name = request.POST.get('name')
            phoneno = request.POST.get('phoneno')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            try:
                form.save()
                send_mail(subject, message, email, ['jashanmakkar62@gmail.com'], name)
                messages.add_message(request, messages.INFO, 'Submitted.')
                return redirect('/email_success')
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            return redirect('/email_success')
        else:
            form = contactform()
        return render(request, 'contact.html', {'form': form})


def email_success(request):
    context = {}
    template = 'email_success.html'
    return render(request, template, context)


def edit(request, id):
    con = contact.objects.get(id=id)
    return render(request, 'edit.html', {'con': con})


def update(request, id):
    con = contact.objects.get(id=id)
    form = contactform(request.POST, instance=con)
    if form.is_valid():
        form.save()
        return redirect("/contact")
    return render(request, 'edit.html', {'con': con})


def destroy(request, id):
    con = contact.objects.get(id=id)
    con.delete()
    return redirect("/")


def insertproduct(request):
    if request.method == "POST":
        form = Productform(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('/insertproduct/')
            except:
                pass
    else:
        form = Productform()
    return render(request, 'addproduct.html', {'form': form})


class CategoryListView(ListView):
    model = category
    template_name = "category.html"


class SubcategoryListView(ListView):
    model = subcategory
    template_name = "subcategory.html"


class ProductListView(object):
    pass


def show(request, cat):
    pro = Product.objects.filter(subcategory=cat)
    subcat = subcategory.objects.get(id=cat)
    cart_product_form = CartAddProductForm()
    context = {
        'pro': pro,
        'subcat': subcat,
        'cart_product_form': cart_product_form
    }
    return render(request, "product.html", context)


def header(request):
    category_list = category.objects.all()
    context_dict = {'cat': category_list, }
    return render(request, 'base.html', context_dict)

def product(request):
    products = Product.objects.all()
    paginate_by = 10
    context = {
        'products': products,
    }
    return render(request, 'product.html', context)

@login_required(login_url='/login/')
def productView(request, myid):
    products = Product.objects.filter(id=myid)
    product = Product.objects.get(id=myid)
    cart_product_form = CartAddProductForm()

    context = {
        'products': products,
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, "productview.html", context)


def search(request):
    global cart_product_form
    produ = None
    query = None
    if 'q' in request.GET and request.GET['q']:
        query = request.GET.get('q')
        produ = Product.objects.all().filter(Q(name__icontains=query) | Q(description__icontains=query))
        cart_product_form = CartAddProductForm()
    else:
        produ = Product.objects.order_by('published_on')
    return render(request, 'search.html', {'query': query, 'produ': produ, 'cart_product_form': cart_product_form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=raw_password)
            if user is not None:
                auth.login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                if 'next' in request.POST:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect('/')
                return redirect('/')
            else:
                messages.success(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'registration/login.html')
    form = AuthenticationForm()
    return render(request=request,
                  template_name="registration/login.html",
                  context={"form": form})


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = auth.authenticate(username=username, password=raw_password)
            auth.login(request, user)
            messages.info(request, f" Dear {username}!, You are registered in fabtrends")
            return redirect('/')
    else:
        form = SignUpForm()

    context = {'form': form}
    return render(request, 'registration/sign.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Youre now logged out')
    return redirect('/')


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have edited your profile')
            return redirect('/')
    else:  # passes in user information
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'registration/edit_profile.html', context)


# return render(request, 'authenticate/edit_profile.html',{})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'You have edited your password')
            return redirect('/')
    else:  # passes in user information
        form = PasswordChangeForm(user=request.user)

    context = {'form': form}
    return render(request, 'registration/change_password.html', context)


@login_required
def feedback(request):
    if request.method == 'POST':
        form = feedbackform(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your Feedback is Submitted')
                return redirect('/')
            except:
                pass
    else:
        form = feedbackform()
    return render(request, 'feedback.html', {'form': form})


def insertquery(request):
    if request.method == 'POST':
        form = queryform(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your Query is Submitted')
                return redirect('/')
            except:
                pass
    else:
        form = queryform()
        return render(request, 'query.html', {'form': form})


def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


def insertprofile(request):
    if request.method == "POST":
        form = profileform(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.add_message(request, messages.INFO, 'Submitted.')
                return redirect('/')
            except:
                pass
    else:
        form = contactform()
    return render(request, 'register/signup.html', {'form': form})


def all_products(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    cart_product_form = CartAddProductForm()
    context = {
        'title' : 'All Products',
        'products': products,
        'cart_product_form': cart_product_form,
    }
    return render(request,'all_products.html',context)
    
    
class refundpageview(TemplateView):
    template_name = "refund.html"
    
def refund(request):
    if request.method == 'POST':
        form = refundform(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your refund request is Submitted')
                return redirect('/')
            except:
                pass
    else:
        form = refundform()
    return render(request, 'refund.html', {'form': form})