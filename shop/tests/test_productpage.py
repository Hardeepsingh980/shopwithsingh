from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product, Category


class TestProductPage(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_title='Test', product_headline='Test',product_img='https://docs.djangoproject.com/en/3.1/_images/django_unittest_classes_hierarchy.svg', product_price=12, product_desc='123', product_category=Category.objects.create(category_name='Test'))
        self.username = 'Test'
        self.password = 'password'
        self.user = User.objects.create_user(self.username,password=self.password)

    def test_product_page_url(self):
        response = self.client.get(f"/shop/{self.product.product_id}", follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, template_name='shop/productdetail.html')

    def test_product_page_name(self):
        response = self.client.get(reverse('productDetail', args=(self.product.product_id,)), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='shop/productdetail.html')

    def test_adding_review(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('review'), data={
            'product_id': self.product.product_id,
            'stars': 5,
            'review_comment': 'Great Product',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.product.product_reviews.count(), 1)
        self.assertEqual(self.product.product_reviews.all()[0].review_comment, 'Great Product')

    def test_add_to_favourites(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('addfav'), data={
            'product_id': self.product.product_id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.favourites.products.count(), 1)
        self.assertEqual(self.user.favourites.products.all()[0], self.product)
        

