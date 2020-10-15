from decimal import Context
from itertools import product
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError

from django_filters.views import FilterView

from .models import Product, Category 
from .forms import OrderForm, AddToCartForm
from .filters import ProductFilter


class ProductListView(FilterView):
    '''
    List view for products with filter by category.
    '''
    model = Product
    filterset_class = ProductFilter
    paginate_by = 6
    template_name = 'products-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_items"] = count_cart_items(self.request)
        return context
    


def add_to_cart(request, slug, quantity):
    '''
    Add item to session based cart. If item already in cart
    change the amount of items to quantity value.
    '''
    # product = Product.objects.get(slug=slug)
    cart = request.session.setdefault('cart', dict())
    cart[slug] = quantity
    request.session.modified = True
    messages.add_message(request, messages.SUCCESS, 'Added to cart.')


def remove_from_cart(request, slug):
    '''
    Remove item from cart.
    '''
    try:
        del request.session['cart'][slug]
        request.session.modified = True
    except KeyError:
        messages.add_message(request, messages.WARNING, 'Something go wrong.')
    else:
        messages.add_message(request, messages.SUCCESS, 'Removed from cart.')


def get_cart_items(request):
    '''
    Return items in cart, if cart is empty return None
    '''
    return request.session.get('cart', None)


def count_cart_items(request):
    '''
    Return count of unique products in cart.
    '''
    items = get_cart_items(request)
    return len(items) if items else 0


def product_detail_view(request, slug):
    '''
    Product detail view. Show product image,
    name, description text, and form to add it to cart.
    '''
    product = get_object_or_404(Product, slug=slug)
    form = None
    if request.method == 'GET':
        form = AddToCartForm(initial={'quantity':request.GET.get('quantity', 1)})
    elif request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            add_to_cart(request, slug, form.cleaned_data['quantity']) #TODO: передавать в посте сколько предметов нужно добавить
            return redirect('shop:detail', slug=slug)
        messages.add_message(request, messages.WARNING, 'Something go wrong.')

    context = {'product':product, 'form':form, 'cart_items':count_cart_items(request)}
    return render(request, 'product-detail.html', context)


def cart_view(request):
    '''
    View for rendering cart.
    '''
    items = None
    cart = request.session.get('cart',[])
    items = Product.objects.filter(slug__in=cart)
    price = 0.0
    for i in items:
        i.item_count = cart[i.slug]
        price = i.price * i.item_count 
    context = {'objects_list':items, 'total_price':price, 'cart_items':count_cart_items(request)}
    return render(request, 'cart.html', context)


def delete_item_view(request, slug):
    '''
    View to confirm that you want to remove current item
    from cart.
    '''
    object = None
    if request.method == 'POST':
        remove_from_cart(request, slug)
        return redirect('shop:cart')
    else:
        object = Product.objects.get(slug=slug)

    context = {'item':object}
    return render(request, 'remove-item.html', context)



def order_view(request):
    cart = request.session.get('cart', None)
    if not cart:
        messages.add_message(request, messages.ERROR, 'Problems with cart.')
        redirect('shop:cart')
    items = Product.objects.filter(slug__in=cart)

    if request.method == 'POST':
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():
            order = order_form.save()
            for i in items:
                order.items.add(i, through_defaults={'item_quantity':cart[i.slug]})
            order.price = order.calc_price()
            order.save()
            del request.session['cart']
            request.session.modified = True
            try:
                send_mail('New order', f'There is new order, order_id:{order.id}', 'admin@example.com', ['admin@example.com'])
                messages.add_message(request, messages.SUCCESS, 'Message sent')
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message not sent')
            return redirect('shop:order-created')
    else:
        order_form = OrderForm()
    
    total_price = 0
    for i in items:
        i.item_count = cart[i.slug]
        total_price += i.price * i.item_count 

    context = {'order_form':order_form, 'total_price':total_price, 'cart_items':count_cart_items(request)}
    return render(request, 'order.html', context)
