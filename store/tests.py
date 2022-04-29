from http import HTTPStatus
from unittest import skip


from importlib import import_module
from django.conf import settings
# This modeule is a wrapper around python unittest package
#When test, a new db is created which contains testing data
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product

from .views import product_all



class TestCategoryModel(TestCase):
    #Creating db for test data
    def setUp(self):
        self.data1 = Category.objects.create(name='django', slug='django')

    def test_category_model_entry(self):

        data = self.data1
        self.assertTrue(expr= isinstance(data, Category))
        self.assertEqual(str(data), 'django')


class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')
        # self.data2 = Product.products.create(category_id=1, title='django advanced', created_by_id=1,
                                            #  slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')
# @skip("demonstrating skipping")
# class TestSkip(TestCase):
#     def test_skip_example(self):
#         pass


class TestViewResponse(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='django', slug='django')
        User.objects.create(username='admin')
        self.data1 = Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                            slug='django-beginners', price='20.00', image='django')

        

    def test_url_allowed_hosts(self):
        """Test Homepage response status"""
        response = self.c.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args= ['django-beginners']))
        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_category_detail_url(self):
        response = self.c.get(reverse('store:category_list', args= ['django']))
        self.assertEqual(response.status_code, HTTPStatus.OK)


    def test_homepage_url(self):
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        
    def test_view_function(self):
        request = self.factory.get('/django-beginners')
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_homepage_html(self):
        """
        Example: code validation, search HTML for text
        """
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>BookStore</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)