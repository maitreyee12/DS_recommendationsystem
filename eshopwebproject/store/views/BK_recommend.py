from django.views import View
from django.shortcuts import render , redirect , HttpResponseRedirect
from store.models.customer import Customer
from store.models.feedback import Feedback
from store.models.product import Products
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
from django.db.models import Avg
import ast
class Recommend(View):
    user_ratings = None
    all_products_rated = None
    
    def get(self, request):
        data = {}
        user_preferences = {}
        arr =[]
        customer_id = request.session.get('customer')
        user_scores = collaborative_filtering(customer_id)
        recommended_product_ids = [product_id for product_id, _ in user_scores[:5]]
        
        for r in recommended_product_ids:
            arr.append(r.id)
        print("recommended_product_ids ",arr)
        recommended_products = Products.objects.filter(id__in=arr)
    
      
        data['products'] = recommended_products
        print(data)
        return render(request, 'recommend.html',data)
    
    
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


def calculate_product_scores(products):
    product_scores = []
    for product in products:
        average_rating = Feedback.objects.filter(product=product).aggregate(Avg('ratings'))['rating__avg']
        if average_rating is not None:
            product_scores.append((product, average_rating))
    return sorted(product_scores, key=lambda x: x[1], reverse=True)
  
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