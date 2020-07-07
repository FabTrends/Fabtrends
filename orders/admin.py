import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Order, OrderItem,Refund,CheckZipcode
from django.urls import reverse
from django.utils.safestring import mark_safe


 
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime.datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin_order_detail', args=[obj.id])))
order_detail.allow_tags = True

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf', args=[obj.id])))
order_pdf.allow_tags = True
order_pdf.short_description = 'PDF bill'
#order_pdf.short_description = 'Invoice'





def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)

make_refund_accepted.short_description = 'Update orders to refund granted'

def make_order_is_shipped(modeladmin, request, queryset):
    queryset.update(in_transit=False, shipped=True)

make_order_is_shipped.short_description = 'Update order from in transit to shipped'


def make_order_is_delivered(modeladmin, request, queryset):
    queryset.update(out_for_delivery=False, delivered=True)

make_order_is_delivered.short_description = 'Update order out for delivery to delivered'

def make_order_is_returned(modeladmin, request, queryset):
    queryset.update(delivered=False, returned=True)

make_order_is_returned.short_description = 'Update order from delivered to return'


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','order_id', 'first_name', 'last_name', 'email','phone_number','town','country','state',
                    'full_address', 'postal_code', 'city', 'paid',
                    'created', 'updated', order_detail, order_pdf, 'shipped',
                    'out_for_delivery',
                    'delivered',
                    'returned',
                    'canceled',
                    'refund_requested',
                    'refund_granted',]
    list_filter = ['paid', 'created', 'updated','shipped',
                    'out_for_delivery',
                    'delivered',
                    'returned',
                    'canceled',
                    'refund_requested',
                    'refund_granted',
                    ]
    list_editable = ('shipped',
                    'out_for_delivery',
                    'delivered',
                    'returned',
                    'canceled',
                    'refund_requested',
                    'refund_granted',
                     )
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    search_fields = ('user__username', 'order_id')
    actions = [make_refund_accepted, make_order_is_shipped, make_order_is_delivered, make_order_is_returned]


admin.site.register(Refund)
admin.site.register(Order, OrderAdmin)

class CheckZipcodeForDelivery(admin.ModelAdmin):
    search_fields = ('zipcode',)

admin.site.register(CheckZipcode, CheckZipcodeForDelivery)

