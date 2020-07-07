from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Order, OrderItem,Refund
from .forms import OrderCreateForm
from .tasks import order_created
from cart.cart import Cart
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RequestRefundForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages

@login_required(login_url='/login/')
def order_create(request):
    global order
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
        return render(request, 'pay.html', {'order': order})
        #return redirect('/')
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'form': form})

def order_created(request):
    
    return render(request, 'orders/order/created.html', {'form': form})



@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    return render(request,
                  'orders/order/detail.html',
                  {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(settings.STATICFILES_DIRS[0] + '/css/pdf.css')])
    return response


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RequestRefundForm()
        context = {
            'form': form
        }
        return render(self.request, "refund.html", context)

    def post(self, *args, **kwargs):
        form = RequestRefundForm(self.request.POST)
        if form.is_valid():
            order_id = form.cleaned_data.get('order_id')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try:
                order = Order.objects.get(order_id=order_id)
                order.refund_requested = True
                order.save()

                #store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(self.request, "Your request has been submitted and our team will get in contact with you")
                return redirect('/')

            except ObjectDoesNotExist:
                messages.warning(self.request, "This order does not exists")
                return redirect('/')

        
def get_zipcode(request, zipcode):
    try:
        checkzip_qs = CheckZipcode.objects.get(zipcode=zipcode)
        messages.success(request, "This product is available at your location")
        return zipcode
    except ObjectDoesNotExist:
        messages.warning(request, "This product is not available at your location")
        return redirect('/')


class CheckZipcodeView(View):
    def post(self, *args, **kwargs):
        form = CheckZipcodeForm(self.request.POST or None)
        if form.is_valid():
            try:
                zipcode = form.cleaned_data.get('zipcode')
                checkzip_qs = get_zipcode(self.request, zipcode)
                return redirect('/')
            except ObjectDoesNotExist:
                return redirect('/')