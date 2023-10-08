from django.views import View
from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.customer import Customer
from store.models.category import Category
from store.models.feedback import Feedback
from store.models.product import Products
from store.models.orders import Order
from django.db.models import Count
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from collections import defaultdict
# from django.db.models import Avg
import ast
class Recommend(View):
    user_ratings = None
    all_products_rated = None
    
    def get(self, request):
        data = {}
        user_preferences = {}
        arr =[]
        customer_id = request.session.get('customer')
        
        customer_orders = Order.objects.filter(customer=customer_id)
        if(customer_orders):
            
            predicted_favorite_category = calculate_predicted_favorite_category(customer_id)
            # Get recommendations from the predicted favorite category
            recommendations = get_recommendations_from_category(predicted_favorite_category,customer_id)
            #print("recommendations ",recommendations)
            context = {
            'favorite_category': predicted_favorite_category,
            'products': recommendations
            }
            data['products'] = recommendations
        else:
            
            mostpopular_prods = get_mostpopular_products()
            #print("mostpopular_prods ",mostpopular_prods)
            context = {
            'favorite_category': None,
            'products': mostpopular_prods
            }
        
    
    
        # print(data)
        return render(request, 'recommend.html',context)


def get_mostpopular_products():
    # this function gives top5 most popular products based on their ratings
    
    # Aggregate the data to count the number of ratings for each product
    product_ratings = Feedback.objects.values('product_id').annotate(rating_count=Count('product_id'))

    # Sort the products based on the rating count in descending order
    sorted_products = sorted(product_ratings, key=lambda x: x['rating_count'], reverse=True)

    # Retrieve the top 5 most popular products
    top_5_popular_products = Products.objects.filter(id__in=[item['product_id'] for item in sorted_products[:5]])

    # Now top_5_popular_products contains the top 5 most popular products
    
    return top_5_popular_products


def calculate_predicted_favorite_category(user_id):
    # Calculate average ratings for each category based on user's orders and ratings
    # user_orders = Order.objects.filter(customer=user_id)
    user_orders = Feedback.objects.filter(customer=user_id)
    category_ratings = {}  # {category_id: [ratings]}
    # print("user_orders ",user_orders)
    for order in user_orders:
        print("each order ",order.product_id.category.id)
            
    for order in user_orders:
        # print("order ",order)
        # for item in order.items.all():
        # print("item ",order)
        category_id = order.product_id.category.id
        if category_id not in category_ratings:
            category_ratings[category_id] = []
        category_ratings[category_id].append(order.ratings)
    
    # Calculate average ratings for each category
    average_category_ratings = {
        category_id: sum(ratings) / len(ratings) for category_id, ratings in category_ratings.items()
    }
    
    # Find the category with the highest average rating
    predicted_favorite_category_id = max(average_category_ratings, key=average_category_ratings.get)
    
    return Category.objects.get(id=predicted_favorite_category_id)




def get_recommendations_from_category(category,customer_id):
    user_orders = Order.objects.filter(customer=customer_id)
    
    # products_asper_fav_category = Products.objects.filter(category=category)
    ordered_product_ids = set(
        order.products.id for order in user_orders 
    )
    # rec = {}
     
    recommendations = Products.objects.filter(category=category).exclude(id__in=ordered_product_ids).order_by('-id')[:5]
  
    
    # print("recommendations ",rec)
    # res = sorted(recommendations, key = lambda x: x[1], reverse = True)[:5]
    # print("recommendations ",recommendations)
    return recommendations
    
def collaborative_filtering(userid):
    user_feedback = Feedback.objects.filter(customer=userid)
    user_rated_product_ids = [feedback.product_id for feedback in user_feedback]
    
    product_ratings = defaultdict(list)
    for feedback in Feedback.objects.exclude(customer=userid):
        if feedback.product_id not in user_rated_product_ids:
            product_ratings[feedback.product_id].append(feedback.ratings)
    
    product_scores = []
    for product_id, ratings in product_ratings.items():
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            product_scores.append((product_id, average_rating))
    
    return sorted(product_scores, key=lambda x: x[1], reverse=True)


# def calculate_product_scores(products):
#     product_scores = []
#     for product in products:
#         average_rating = Feedback.objects.filter(product=product).aggregate(Avg('ratings'))['rating__avg']
#         if average_rating is not None:
#             product_scores.append((product, average_rating))
#     return sorted(product_scores, key=lambda x: x[1], reverse=True)
  
def recommend_products(customer_id):
        # Fetch user ratings
    user_ratings = Feedback.objects.filter(customer=Customer(id = customer_id))

    # Calculate average ratings for each product
    product_ratings = {}
    for rating in user_ratings:
        product_id = rating.product_id
        if product_id not in product_ratings:
            product_ratings[product_id] = []
        product_ratings[product_id].append(rating.ratings)
    
    # Calculate average ratings
    average_ratings = {}
    for product_id, ratings in product_ratings.items():
        average_ratings[product_id] = sum(ratings) / len(ratings)

    # Sort products by average rating (descending order)
    sorted_products = sorted(average_ratings.keys(), key=lambda x: average_ratings[x], reverse=True)

    # Retrieve recommended products
    recommended_products = Products.objects.filter(id__in=sorted_products[:5])  # Get top 5 recommended products
    for rp in recommended_products:
        print(rp.name)
    context = {
        'products': recommended_products,
    }
    
    return  recommended_products