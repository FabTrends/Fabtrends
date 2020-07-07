from django.conf.urls import url
from . import views
from django.urls import path, include
app_name = 'orders'

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^created/$', views.order_created, name='order_created'),
    #url(r'^my_orders/$', views.my_orders, name='my_orders'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/order/<int:order_id>/pdf/', views.admin_order_pdf, name='admin_order_pdf'),
    path('check-zipcode/', views.CheckZipcodeView.as_view(), name='check-zipcode'),
    path('refund-request/', views.RequestRefundView.as_view(), name='refund-view'),
     
]