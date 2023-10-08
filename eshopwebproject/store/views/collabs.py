from django.shortcuts import render , redirect
from store.models.session import Sessions
from django.contrib.auth.hashers import  check_password
from store.models.product import Products
from store.models.category import Category
from store.models.session import Sessions
from store.models.feedback import Feedback
from store.models.customer import Customer
from store.models.customerInteraction import CustomerInteractions
from django.views import  View
from store.models.product import Products
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Collabs(View):
    def get(self, request):
        products = product_recommendation(request.session.get('customer'))
        return render(request , 'collabs.html',{'products':products} )


def product_recommendation(user_id, num_recommendations=5):
    users = Customer.objects.all()
    # products = Products.objects.all()
    products = Products.get_all_products();
    user_bought_products = set(Feedback.objects.filter(customer__id=user_id).values_list('product_id__id', flat=True))
    # Determine the maximum user and product IDs in your dataset
    max_user_id = max(Feedback.objects.values_list('customer__id', flat=True))
    max_product_id = max(Feedback.objects.values_list('product_id__id', flat=True))
    # Create a user-product matrix
    # user_product_matrix = np.zeros((users.count(), products.count()))
    user_product_matrix = np.zeros((max_user_id,max_product_id))
    # Fill the user-product matrix with ratings
    for rating in Feedback.objects.all():
        custid = rating.customer
        user_product_matrix[rating.customer.id - 1, rating.product_id.id - 1] = rating.ratings
    
    # Calculate user similarity using cosine similarity
    user_similarity = cosine_similarity(user_product_matrix)
    
    # Get the target user's similarity vector
    target_user_similarity = user_similarity[user_id - 1]  
    # Find similar users
    #similar_users = target_user_similarity.argsort()[-num_recommendations-1:-1][::-1]
    #exclusive_similar_users = [user_idx for user_idx in similar_users if user_idx + 1 != user_id]  # Exclude current user
    # Find similar users
    similar_users = target_user_similarity.argsort()[-num_recommendations-1:-1][::-1]
    # Exclude the current user
    exclusive_similar_users = [user_idx +1 for user_idx in similar_users if user_idx + 1 != user_id]

# # Debugging statements
    print("similar_users (after exclusion): ", exclusive_similar_users)
    # Collect products rated by similar users that the target user hasn't rated
    recommendations = []
    for user_idx in exclusive_similar_users:
        rated_products = [rating.product_id.id - 1 for rating in Feedback.objects.filter(customer=user_idx + 1)]
        unrated_products = np.where(user_product_matrix[user_id - 1] == 0)[0]
        for product_idx in rated_products:
            if product_idx in unrated_products and products[product_idx].id not in user_bought_products:
                recommendations.append(products[product_idx])
                if len(recommendations) >= num_recommendations:
                    break
        
        if len(recommendations) >= num_recommendations:
            break
    return recommendations
