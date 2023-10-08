from django.contrib import admin
from django.urls import path
from .views.home import Home , store, showproduct_details
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.interactions_recomms import Interactions_Recomms
from .views.collabs import Collabs
from .views.checkout import CheckOut
from .views.orders import OrderView, order_details
from .views.order_details import OrderDetailsView
from .views.recommend import Recommend
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Home.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('userinteractions', Interactions_Recomms.as_view(), name='userinteractions'),
    path('collabfiltering', Collabs.as_view(), name='collabfiltering'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('recommend', Recommend.as_view() , name='recommend'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),
    path('order_details', order_details, name='order_details'),
    path('save_ratings/<int:product_id>/', OrderDetailsView.as_view(), name='save_ratings'),
    path('productdetails', showproduct_details, name='productdetails'),

]