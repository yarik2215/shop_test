from django.core.handlers.wsgi import WSGIRequest
from django.http import response
from django.http.request import HttpRequest
from django.test import client
from django.test.testcases import SimpleTestCase
from django.test import TestCase
from django.utils.text import slugify
from shop_app import views

# Create your tests here.

from shop_app.models import Category, Product
from django.urls import reverse


def add_product(name : str, price : float, category : Category = None):
    return Product.objects.create(name=name, 
                slug=slugify(name), price=price, description=f'Description', 
                image='/media/image.png', category=category)


class ProductListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        num_products = 13
        for i in range(num_products):
            add_product(f'Product {i}', 1.50)

    def test_view_url_exists_at_desired_location(self): 
        resp = self.client.get('/products/') 
        self.assertEqual(resp.status_code, 200)  
           
    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('shop:list'))
        self.assertEqual(resp.status_code, 200)

    def test_pagination_is_six(self):
        resp = self.client.get(reverse('shop:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['product_list']) == 6)



class ProductDetailView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.obj = add_product('Product 1', 12.0)

    def test_product_detail_correct(self):
        response = self.client.get(reverse('shop:detail', args=['product-1']))                         
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'],
                                    self.obj)

    def test_product_detail_that_doesnt_exist_correct(self):
        response = self.client.get(reverse('shop:detail', args=['product-2']))
        self.assertEqual(response.status_code, 404)
        
    def test_product_detail_add_to_cart_request(self):
        response = self.client.post(reverse('shop:detail', args=['product-1']),
                                    data = {
                                        'quantity' : 3,
                                    })
        self.assertRedirects(response, reverse('shop:detail', args=['product-1']))
        self.assertEqual(self.client.session.get('cart'), {'product-1' : 3})

    def test_product_detail_add_to_cart_request_incorrect_amount(self):
        response = self.client.post(reverse('shop:detail', args=['product-1']),
                                    data = {
                                        'quantity' : 0,
                                    })   
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(self.client.session.get('cart'))

    def test_product_detail_add_to_cart_item_that_not_exist(self):
        response = self.client.post(reverse('shop:detail', args=['product-2']),
                                    data = {
                                        'quantity' : 1,
                                    })   
        self.assertEqual(response.status_code, 404)
 


def fill_cart_with_items(session):
    session['cart'] = dict()
    cart = session['cart']
    for i in range(3):
        obj = add_product(f'Product {i}', 1.50)
        cart[obj.slug] = 3
    session.save()


class CartViewTest(TestCase):

    def test_cart_view_empty(self):
        response = self.client.get(reverse('shop:cart'))
        self.assertFalse(response.context['objects_list'])

    def test_cart_view_with_items(self):
        fill_cart_with_items(self.client.session)
        response = self.client.get(reverse('shop:cart'))
        self.assertQuerysetEqual(response.context['objects_list'], 
                                    ['<Product: Product 0>','<Product: Product 1>','<Product: Product 2>'])



class OrderViewTest(TestCase):

    def test_order_view(self):
        fill_cart_with_items(self.client.session)
        response = self.client.get(reverse('shop:order'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order.html')

    def test_order_view_create_order_correct_data(self):
        fill_cart_with_items(self.client.session)
        response = self.client.post(reverse('shop:order'), data={
                                        'first_name' : 'Bob',
                                        'last_name' : 'Bobston',
                                        'email' : 'bob@mail.com',
                                        'phone' : '380959484855',
                                        'comment' : 'Some text.',
                                    })
        self.assertRedirects(response, reverse('shop:order-created'))

    def test_order_view_create_order_incorrect_data(self):
        fill_cart_with_items(self.client.session)
        response = self.client.post(reverse('shop:order'), data={})
        self.assertTrue(response.context['order_form'].errors)



