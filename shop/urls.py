from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.productDetail, name='productDetail' ),
    path('search/', views.search, name='search'),
    path('favourites/', views.favourites, name='favourites'),
    path('addfav/', views.addtofavourites, name='addfav'),
    path('removefav/', views.removefav, name='removefav'),
    path('trackorder/', views.trackorder, name='trackorder' ),
    path('review/', views.review, name="review"),
    path('buynow/', views.buy_now, name="buynow"),
    path('checkout/', views.checkout, name="checkout"),
    path('charge/', views.charge, name="charge")
]