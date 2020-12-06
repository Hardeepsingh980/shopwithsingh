from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Product, Category


class TestBuyProduct(TestCase):
    def setUp(self):
        self.product = Product.objects.create(product_title='Test', product_headline='Test',product_img='https://docs.djangoproject.com/en/3.1/_images/django_unittest_classes_hierarchy.svg', product_price=12, product_desc='123', product_category=Category.objects.create(category_name='Test'))
        self.username = 'Test'
        self.password = 'password'
        self.user = User.objects.create_user(self.username,password=self.password)

    # def test_buy_product(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.post(reverse('buynow'), data={
    #         'product_id': self.product.product_id,
    #         'stars': 5,
    #         'review_comment': 'Great Product',
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(self.product.product_reviews.count(), 1)
    #     self.assertEqual(self.product.product_reviews.all()[0].review_comment, 'Great Product')