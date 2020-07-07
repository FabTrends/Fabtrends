from django.urls import path
from fabtrendapp import views
from django.contrib.auth import views as auth_views
app_name = "fabtrendapp"

urlpatterns = [

    path('', views.indexpageView.as_view(), name='index'),
    path('base/', views.basepageView.as_view()),
    path('contact/', views.contactpageView.as_view(), name='contact'),
    path('checkout/', views.checkoutpageView.as_view(), name='checkout'),
    path('privacy/', views.privacypageView.as_view(), name='privacy'),
    path('addproduct/', views.addproductpageview.as_view()),
    path('FAQs/', views.FAQspageView.as_view(), name='faqs'),
    path('about/', views.aboutpageView.as_view(), name='about'),
    path('delete/<int:id>', views.destroy),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('insert/', views.insert),
    path('list/', views.listView.as_view()),
    path('product/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('email_success/', views.email_success, name='email_success'),
    path('category/', views.CategoryListView.as_view(), name='categorylist'),
    path('subcategory/', views.SubcategoryListView.as_view(), name='subcategorylist'),
    path('product/', views.productpageView.as_view()),
    path('product/<int:cat>/', views.show),
    path('insertproduct/', views.insertproduct,name="insertproduct"),
    path('products/<int:myid>', views.productView, name="productView"),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('login/', views.login, name='login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('query/', views.querypageview.as_view(),name='query'),
    path('feedback',views.Feedbackpageview.as_view(),name="feedback"),
	path('insertfeedback',views.feedback),
    path('insertquery/',views.insertquery),
    path('all_products/', views.all_products , name='all_products'),
]
