from django.contrib import admin
from fabtrendapp.models import category, subcategory, Product, contact, FAQs, feedback, query



@admin.register(category)
class categoryAdmin(admin.ModelAdmin):
    pass


@admin.register(subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'subcategory', 'published_on', 'discounted_price', 'price')
    list_editable = ['price']
    list_filter = ['price']
    readonly_fields = ['updated']
    list_select_related = ('subcategory',)
    search_fields = ['name', ]
    list_per_page = 25
    pass


@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    fields = ["phoneno", "name", "subject", "message"]
    list_display = ["id", "name", "phoneno", "subject", "message", "created_at"]
    search_fields = ["name"]
    list_filter = ["created_at", "name"]
    list_editable = ["name"]


@admin.register(FAQs)
class FAQsAdmin(admin.ModelAdmin):
    pass


@admin.register(feedback)
class feedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'comments',)


@admin.register(query)
class queryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'query',)