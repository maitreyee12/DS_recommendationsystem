from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.customerInteraction import CustomerInteractions 

from store.models.product import Products
from store.models.orders import Order
from store.models.session import Sessions


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_idList(list(cart.keys()))
       
        for product in products:
            order = Order(customer=Customer(id=customer),
                          products=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            purchaseInteraction(product.id,customer)
        sessionobj = Sessions(custid=request.session.get('customer'),
                                          session_products= cart)
        sessionobj.remove_session(request.session.get('customer'))
        request.session['cart'] = {}

        return redirect('cart')
    
def purchaseInteraction(product_id,customer_id):
    print("purchaseInteraction",product_id,customer_id)
    userInteractionObj = CustomerInteractions(customer=Customer(id=customer_id),product= Products(id=product_id),interaction_type="purchase")
    userInteractionObj.saveInteraction()
    return None
