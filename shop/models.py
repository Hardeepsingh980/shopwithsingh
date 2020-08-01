from django.db import models
from django.contrib.auth.models import User


class Sizes(models.Model):
    size_id = models.AutoField(primary_key=True)
    size_name = models.CharField(max_length=5)

    def __str__(self):
        return self.size_name


class Color(models.Model):
    color_id = models.AutoField(primary_key=True)
    color_name = models.CharField(max_length=10)
    color_code = models.CharField(max_length=15)

    def __str__(self):
        return self.color_name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_product = models.ForeignKey('Product', on_delete=models.CASCADE)
    review_comment = models.CharField(max_length=100)
    review_stars = models.IntegerField(
        choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    review_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_user.username

    def save(self, *args, **kwargs):
        super(Review, self).save(*args, **kwargs)
        self.review_product.product_reviews.add(self)
        total_count = 0
        total_av = 0
        for i in self.review_product.product_reviews.all():
            total_count += 1
            total_av += i.review_stars

        self.review_product.product_avg_rating = total_av / total_count
        self.review_product.save()


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_title = models.CharField(max_length=30)
    product_headline = models.CharField(max_length=50)
    product_img = models.URLField()
    product_price = models.IntegerField()
    product_count = models.IntegerField(default=1)
    product_sizes_avalable = models.ManyToManyField(Sizes)
    product_colors_avalable = models.ManyToManyField(Color)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_desc = models.TextField(max_length=1000)
    product_reviews = models.ManyToManyField(Review, blank=True)
    product_avg_rating = models.IntegerField(default=5)

    def __str__(self):
        return self.product_title


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_size = models.ForeignKey(Sizes, on_delete=models.CASCADE)
    order_color = models.ForeignKey(Color, on_delete=models.CASCADE)
    order_amount = models.IntegerField()
    order_quantity = models.IntegerField()
    order_payment_type = models.CharField(max_length=10,
        choices=(('COD', 'COD'), ('ONLINE', 'ONLINE')))
    order_payment_due = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_updated_at = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=20, choices=(('Processing', 'Processing'), (
        'Dispatched', 'Dispatched'), ('On the way', 'On the way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')), default='Processing')
    
    def __str__(self):
        return f'{self.order_user.username} ordered {self.order_product.product_title}'
    
