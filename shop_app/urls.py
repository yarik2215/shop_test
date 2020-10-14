from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'shop'
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='list'),
    path('products/<slug:slug>', views.product_detail_view, name='detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/delete/<slug:slug>', views.delete_item_view, name='delete'),
    path('order/', views.order_view, name='order'),
    path('order/created/', TemplateView.as_view(template_name='order-created.html'), name='order-created'),
]