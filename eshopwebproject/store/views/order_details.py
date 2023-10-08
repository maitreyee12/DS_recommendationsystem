from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.product import Products
from store.models.orders import Order
from store.models.feedback import Feedback
from store.middlewares.auth import auth_middleware
import ast
class OrderDetailsView(View):
    orderinfo = {}
    ratings = None
    
    def get(self, request, product_id):
        # OrderDetailsView.orderinfo = request.GET.get('orderinfo')
        print("product_id")
        print(product_id)
        # Handle GET request here
        # This can be used to display the form for rating or any other GET-related logic
        pass
    
    def post(self, request, product_id):
        print("product_id2")
        print(product_id)
        # Handle POST request here
        # This is where you process the submitted form data and save the ratings
        # You can access the form data using request.POST
        order_id = request.POST.get('orderid')
        orderinfo2 = request.POST.get('orderinfo')
        data_dict = ast.literal_eval(orderinfo2)
        price = data_dict['price']
        quantity = data_dict['quantity']
        rate = request.POST.get('rate')
        save_rates =Feedback(product_id=Products(id=product_id),order_id= Order(id=order_id),customer=Customer(id=request.session.get('customer')),quantity=quantity,
                             price=price,ratings=rate)
        save_rates.saveRatings()
        # ... process the form data and save the ratings ...

        # Redirect back to the same page or a success page
        # return HttpResponseRedirect('order_details.html' + order_id)
        return HttpResponseRedirect('order_details.html' , {'orderinfo': orderinfo2})
    
#     def get(self, request):
#         #print("orderdetails get")
        
#         return render(request, 'order_details.html', {'orderinfo': request.POST.get('orderinfo')})

    

        
# def save_ratings(request, product_id):
#     print("product_id")
#     print(product_id)
#     if request.method == 'POST':
#         value = int(request.POST.get('rate'))
#         print("save_rating")
#         print(value)
#         orderinfo2 = request.POST.get('orderinfo')
#         orderid = request.POST.get('order_id')
#         data_dict = ast.literal_eval(orderinfo2)
#         price = data_dict['price']
#         quantity = data_dict['quantity']
#         orders = Order.get_orders_by_id(orderid)
    
#         for o in orders:
            
#             orderinfo = {
#             "prod_id":o.products.id,
#             "order_id":orderid,
#             "name":o.products.name,
#             "price": o.price,
#             "quantity":o.quantity,
#             "image":o.products.image.url,
#             "desc":o.products.description
#         }
#     #     print("save_rating")
#     #     print(value)
#         print(orderinfo2)
#         print(orderinfo)
#         save_rates =Feedback(product_id=Products(id=product_id),order_id= Order(id=orderid),customer=Customer(id=request.session.get('customer')),quantity=quantity,
#                              price=price,ratings=value)
            
#         save_rates.saveRatings()
#         print(save_rates)
#     return render(request, 'order_details.html', {'orderinfo': orderinfo})
        # rating = Rating.objects.create(value=value)
        # You can add more logic here if needed
        # return render(request, 'order_details.html', {'orderinfo': orderinfo2})