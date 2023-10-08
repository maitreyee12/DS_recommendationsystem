from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.feedback import Feedback
from store.models.product import Products
from store.models.orders import Order
from store.middlewares.auth import auth_middleware
import ast
from django.core.exceptions import ObjectDoesNotExist
class OrderView(View):

    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        prod_rating = []
        feedbacks_obj2=[]
        orders_with_ratings = []
        for ord in orders:

            feedbacks_obj2 = Feedback.objects.filter(order_id=ord.id)
            order_data = {
            'order_number': ord.id,
            'product_id':ord.products.id,
            'product_img':ord.products.image,
            'product_name':ord.products.name,
            'product_date':ord.date,
            'price':ord.price,
            'quantity':ord.quantity,
            'status':ord.status,
            'ratings': [feedback.ratings for feedback in feedbacks_obj2],
            }
            
            orders_with_ratings.append(order_data)
        
        print("prod_rating ",prod_rating)
        return render(request , 'orders.html'  , {'orders_with_ratings' : orders_with_ratings})
    
    def post(self, request):
        customer = request.session.get('customer')
        product_name = request.POST.get('product_name')
        orderID = request.POST.get('orderid')
        return render(request , 'order_details.html', {'orderid' : orderID})
    
    
def fetch_rating(product_id, customer_id, order_id):
    try:
        feedback_obj = Feedback.objects.get(
            product_id=product_id,
            customer=customer_id,
            order_id=order_id
        )
    except ObjectDoesNotExist:
        feedback_obj = None
    return feedback_obj

def order_details(request):
    rate = 0
    order_ID = request.POST.get('orderid')
    prod_id = request.POST.get('prod_id')
    orderinfo2 = request.POST.get('orderinfo')
    feedback_exists = fetch_rating(prod_id,request.session.get('customer'),order_ID)
    
    if(feedback_exists):
        rate = feedback_exists.ratings
    else:
        rate = 0
    if(orderinfo2):
        
        data_dict = ast.literal_eval(orderinfo2)
        price = data_dict['price']
        quantity = data_dict['quantity']
        rate = request.POST.get('rate')
        save_rates =Feedback(product_id=Products(id=prod_id),order_id= Order(id=order_ID),customer=Customer(id=request.session.get('customer')),quantity=quantity,
                             price=price,ratings=rate)
        if(feedback_exists):
            feedbackobj = save_rates.get_feedback_by_id(feedback_exists.id)
            if(feedbackobj):
                feedbackobj.update_feedback(feedbackobj.id,rate)
        else:
            save_rates.saveRatings()
    else:
        print("orderinfo2 else")
        
    orderinfo = {}
    orders = Order.get_orders_by_id(order_ID)
    # feedback_ratings = 
    for o in orders:
        
        orderinfo = {
        "prod_id":o.products.id,
        "order_id":order_ID,
        "name":o.products.name,
        "price": o.price,
        "quantity":o.quantity,
        "image":o.products.image.url,
        "desc":o.products.description,
        "ratings":rate
    }
    return render(request, 'order_details.html', {'orderinfo': orderinfo})
