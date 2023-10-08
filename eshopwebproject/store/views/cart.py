from django.shortcuts import render , redirect
from store.models.session import Sessions
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from django.views import  View
from store.models.product import Products

class Cart(View):
    selected_products = None
    isprod_present = False
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_idList(ids)
        return render(request , 'cart.html' , {'products' : products} )
    
    def post(self, request):
        remove_cart = request.POST.get('cart-remove')
        product = request.POST.get('product')
        cart = request.session.get('cart')
        yesbtn = request.POST.get('yesbtn')
        nobtn = request.POST.get('nobtn')
        if product==None:
            #print("product")
            #print(product)
            if yesbtn:
                #print("yesbtn")
                cart = {}
                Sessions.remove_session(request.session.get('customer'))
            # else:
            #     if nobtn:
            #         print("nobtn")
        else:
            #print("else product")
            if cart:
                quantity = cart.get(product)
                if quantity:
                    if remove_cart:
                        if quantity<=1:
                            cart.pop(product)
                        else:
                            cart[product]  = quantity-1
                    else:
                        cart[product]  = quantity+1
                else:
                    cart[product] = 1
            else:
                cart = {}
                cart[product] = 1

        request.session['cart'] = cart
        #print(cart)
        ids = list(request.session.get('cart').keys())
        products = Products.get_products_by_idList(ids)
        return render(request , 'cart.html' , {'products' : products} )
        #return None