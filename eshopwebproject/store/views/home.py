from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.product import Products
from store.models.category import Category
from store.models.session import Sessions
from store.models.feedback import Feedback
from store.models.customer import Customer
from store.models.orders import Order
from store.models.customerInteraction import CustomerInteractions 
from django.views import View
from store.middlewares.auth import auth_middleware
from django.template import RequestContext
from sklearn.metrics.pairwise import cosine_similarity
# from django.views.decorators.csrf import csrf_protect
from sklearn.feature_extraction.text import TfidfVectorizer

import json
import numpy as np
from django.http import JsonResponse
import ast
#import pdb;

# Create your views here.
class Home(View):
    #pdb.set_trace()
    customername = None
    prods_quants = []
    val = None
    v1=None
    v2=None
    def post(self , request):
        # print(request.session)
        
        csrfContext = RequestContext(request)
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        remove_cart = request.POST.get('cart-remove')
        prod_int = int(product)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
               
                if remove:
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
        sessionobj = Sessions(custid=request.session.get('customer'),
                                          session_products= cart)
        if(len(cart)==0):
            sessionobj.remove_session(request.session.get('customer'))
        else:
            if(sessionobj.is_session_exists(request.session.get('customer'))):
                sessionobj.update_session(sessionobj)
            else:
                sessionobj.saveSession()
        
        if remove_cart:
            return render(request , 'cart.html' , {'products' : cart} )
        else:
            return redirect('homepage')



    def get(self , request):
        csrfContext = RequestContext(request)
        if request.session.get('customer'):
          Home.customername = request.session.get('customername')
          return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}', {'customername' : Home.customername})
        else:
            
            return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')
        


    

def getJsonObj(data1):
        #data = [['9',2],['10',1]]
        # Convert the dictionary to a JSON response
        #json_data = json.dumps(data1)
        json_data = json.loads(data1)
        print("json_data")
        print(json_data)
        return JsonResponse(json_data, safe=False)    
    
   

def find_element_index(matrix, val):
    arr = []
    for index, lst in enumerate(matrix):
        if val in lst:
            print("index, lst.index(val)")
            print( index, lst.index(val) )
            i = index
            prod_i = lst.index(val)
        else:
            return None
    Arr = [i,prod_i]
    return Arr
    

def get_alredy_existed_element(prod,prodsArr):
        #breakpoint()
    print("Home.prods_quants2 ",prodsArr)
    print("PROD ",prod)
    #prod1 = 10
    arr1=prodsArr
    val = prod
    
    i = None
    prod_i = None
    Arr = []
    
    for row in arr1:  # Iterate through rows of the 2D array
        print("ROW ",row)
        for element in row:  # Iterate through elements in each row
            print("element ",element)
            if element == val:  # Compare the element to the target value
                print("Element == prod...")
                ind = arr1.index(element)
                print("IND, ",ind)
                print("ROW2 ",row)
                #ele = find_element_index(arr1, val)
                #print("ELE.. ", element)
                return None
            else:
                return None
   

def store(request):
    
    prods = None
    flat_list = []
    selected_prod_cats = []
    selected_prods_quants = []
    nested_list = {}
    if(request.session.get('customer')):
        print("session_cart")
        prodArr = None
        session_cart = Sessions.get_all_session_id(request.session.get('customer'))
        print(session_cart)
        if session_cart.exists():
            for prods in session_cart:
                    prodArr=(prods.session_products)
                    print(prodArr)
            if(len(prodArr)>0):
                nested_list = ast.literal_eval(prodArr)
            else:
                nested_list = {}
            
        else:
           nested_list = {}

        
        print(nested_list)
        print(type(nested_list))
     
    
    cart = request.session.get('cart')
    print("CART")
    print(cart)
    if not cart:
        cart = nested_list
        #request.session['cart'] = {}
        request.session['cart'] = nested_list
        #request.session['cart'] = flat_list
        #cart = flat_list
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories
    # print("products")
    # print(products)
    if request.session.get('customer'):
          Home.customername = request.session.get('customername')
          data['customername'] = Home.customername
    return render(request, 'index.html', data)


# product_recommendation code shifted to collabs.py

#Content-Based Recommendation Function
def get_content_based_recommendations(product_id, num_recommendations=5):
    # product_descriptions = [product.description for product in Products.objects.all()]
    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(product_descriptions)
    
    # Get product categories for all products
    product_categories = [product.category.name for product in Products.objects.all()]
    # print("product_categories ",product_categories)
    
    # Convert product categories into numerical feature vectors using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(product_categories)
    
    product_index = Products.objects.filter(id=product_id).first().id - 1
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    similar_products = list(enumerate(cosine_sim[product_index]))
    similar_products.sort(key=lambda x: x[1], reverse=True)
    
    recommended_product_indices = [product[0] for product in similar_products[1:num_recommendations + 1]]
    recommended_products = Products.objects.filter(id__in=recommended_product_indices)
    
    return recommended_products

def showproduct_details(request):
    prod_id = request.POST.get('productid')
    # print("prod_id ",prod_id)
    # print("prod_idtype  ",type(prod_id))
    product = Products.get_products_by_id(prod_id)
    customerid = request.session.get('customer') 
    prod_detail = {}
    # saveInteractionToDB(prod_id,customerid)
    userInteractionObj = CustomerInteractions(customer=Customer(id=request.session.get('customer')),product= Products(id=prod_id),interaction_type="view")
    userInteractionObj.saveInteraction()
    for o in product:
        print("OOOO ",o.name)
        print("OOOO ",o.price)
        prod_detail = {
        "prod_id":o.id,
        "name":o.name,
        "price": o.price,
        "category":o.category.name,
        "image":o.image,
        "desc":o.description,
    }
    userid = request.session.get('customer')
    customer_orders = Order.objects.filter(customer=userid)
    if(customer_orders):
        print("orders exists")
        recommended_products = get_content_based_recommendations(prod_id)
        # recommended_products = product_recommendation(userid)
    else:
        print("no orders")
        recommended_products= None

    # recommended_products = product_recommendation(product_id)
    # recommended_products = None
    print("prod_details ",prod_detail)
    return render(request, 'product_details.html', {'product': prod_detail,'rec_prods':recommended_products})