from django.shortcuts import render, redirect
from .models import Product, Review, Order, Color, Sizes
from accounts.models import Address, Favourites
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib import messages


razorpay_client = razorpay.Client(auth=("rzp_test_vmGcASSHfe8gjU", "HhBRTjhmFDGIMzCAPWzcgbN0"))


def productDetail(request, product_id):
    product = Product.objects.get(product_id=product_id)
    return render(request, 'shop/productdetail.html', context={'product':product})

@login_required
def review(request):
    if request.method == 'POST':
        review = Review()
        review.review_product = Product.objects.get(product_id=request.POST['product_id'])
        review.review_stars = request.POST['stars']
        review.review_user = request.user
        review.review_comment = request.POST['review_comment']
        review.save()
        product = Product.objects.get(product_id=request.POST['product_id'])
        messages.success(request, 'Review Added Successfully')
        return redirect('productDetail',product.product_id)
    else:
        return redirect('home')

@login_required
def buy_now(request):
    if request.method == 'POST':
        order = Order()
        order.order_user = request.user
        order.order_product = Product.objects.get(product_id=request.POST['product_id'])
        order.order_color = Color.objects.get(color_id=request.POST['color_id'])
        order.order_size = Sizes.objects.get(size_id=request.POST['size_id'])
        order.order_quantity = request.POST['quantity']
        order_amount = int(order.order_product.product_price) * int(order.order_quantity)
        return render(request, 'shop/checkout.html', context={'order':order, 'order_amount': order_amount})
    else:
        return redirect('home')

@login_required
def checkout(request):
    if request.method == 'POST':
        order = Order()
        order.order_user = request.user
        order.order_product = Product.objects.get(product_id=request.POST['product_id'])
        order.order_color = Color.objects.get(color_id=request.POST['color_id'])
        order.order_size = Sizes.objects.get(size_id=request.POST['size_id'])
        order.order_quantity = int(request.POST['quantity'])
        order.order_amount = int(request.POST['order_amount'])
        order.order_payment_type = request.POST['payment_type']
        try:
            order.order_user.address
        except:
            order.order_user.address = Address()
            order.order_user.save()
        order.order_user.address.country = 'India'
        order.order_user.address.state = request.POST['state']
        order.order_user.address.city = request.POST['city']
        order.order_user.address.pincode = request.POST['pincode']
        order.order_user.address.phone = request.POST['phone']
        order.order_user.address.street_address = request.POST['street_address']
        order.order_user.address.save()
        order.order_user.first_name = request.POST['first_name']
        order.order_user.last_name = request.POST['last_name']
        order.order_user.save()
        order.save()
        if order.order_payment_type == 'ONLINE':
            return render(request, 'shop/paymentpage.html', context={'order': order})
        else:
            return render(request, 'shop/ordersuccess.html', context={'order_id':order.order_id})
    else:
        return redirect('home')

def charge(request):
    if request.method == 'POST':
        try:
            order = Order.objects.get(order_id=request.POST['order_id'])
            amount = order.order_amount * 100
            payment_id = request.POST['razorpay_payment_id']
            razorpay_client.payment.capture(payment_id, amount)
            order.order_payment_due = False
            order.save()
            return render(request, 'shop/ordersuccess.html', context={'order_id':order.order_id})
        except:
            return redirect('home')
    else:
        return redirect('home')

def search(request):
    query = request.GET['query']
    products = Product.objects.filter(product_title__contains=query)
    # products += Product.objects.filter(product_category__contains=query)
    return render(request, 'shop/search.html', context={'products': products, 'query': query})

@login_required
def trackorder(request):
    orders = Order.objects.filter(order_user=request.user)[::-1]
    return render(request, 'shop/trackorder.html', context={'orders':orders})

@login_required
def addtofavourites(request):
    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(product_id=request.POST['product_id'])
        try:
            user.favourites
        except:
            user.favourites = Favourites()
            user.favourites.save()

        user.favourites.products.add(product)
        user.favourites.save()
        messages.success(request, 'Product Added To Favourites')
        return redirect('productDetail',product.product_id)
    else:
        return redirect('home')

@login_required
def favourites(request):
    return render(request, 'shop/favourites.html')

@login_required
def removefav(request):
    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(product_id=request.POST['product_id'])
        user.favourites.products.remove(product)
        user.favourites.save()
        messages.success(request, 'Product Removed From Favourites')
        return redirect('favourites')
    else:
        return redirect('home')


