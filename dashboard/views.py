from datetime import timedelta, date
from django.shortcuts import render, redirect
from shop.models import Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test



def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@user_passes_test(lambda u: u.is_superuser)
def dashhome(request):
    labels = []
    data = []

    orders = Order.objects.all()
    start_date = date(2020, 7, 20)
    end_date = date.today() + timedelta(days=1)
    for single_date in daterange(start_date, end_date):
        labels.append(str(single_date))
        o = 0
        for i in range(0, len(orders.filter(order_date__date=single_date))):
            o += 1
        data.append(o)

    orders_pending = orders.exclude(order_status='Delivered')

    total_users = len(User.objects.all())
    total_orders = len(Order.objects.all())
    total_earned = 0
    for i in Order.objects.all():
        total_earned += i.order_amount

    total_pending = len(orders_pending)


    return render(request, 'dashboard/dashboard.html', {
        'labels': labels,
        'data': data,
        'orders_pending': orders_pending,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_earned': total_earned,
        'total_pending': total_pending
    })


@user_passes_test(lambda u: u.is_superuser)
def updateorder(request):
    if request.method == 'POST':
        order = Order.objects.get(order_id=request.POST['order_id'])
        status = request.POST['status']
        order.order_status = status
        order.save()
        messages.success(request, 'Order updated')
        return redirect('dashboard')
    else:
        return redirect('dashboard')