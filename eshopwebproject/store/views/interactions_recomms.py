from django.shortcuts import render , redirect
from store.models.session import Sessions
from django.contrib.auth.hashers import  check_password
from store.models.customer import Customer
from store.models.customerInteraction import CustomerInteractions
from django.views import  View
from store.models.product import Products
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Interactions_Recomms(View):
    def get(self, request):
        products = user_based_history_recommendation(request.session.get('customer'))
        # products = {}
        # for prods in r_products:
        #     products = {
        #         "id":prods.id,
        #         "name":prods.name,
                
        #     }
        # print("products ",products)
        return render(request , 'interactions_recomms.html',{'products':products} )
    

def user_based_history_recommendation(target_user_id):
    print("target_user_id ",target_user_id)
    # Retrieve all users, products, and interactions
    users = Customer.objects.all()
    products = Products.objects.all()
    interactions = CustomerInteractions.objects.all()
    users_list = list(users)
    products_list = list(products)
    # Create a user-product interaction matrix
    interaction_matrix = np.zeros((users.count(), products.count()))
    num_recommendations = 5
    # Populate the interaction matrix
    for interaction in interactions:
        user_idx = users_list.index(interaction.customer)
        product_idx = products_list.index(interaction.product)
        interaction_matrix[user_idx, product_idx] = 1  # You can use different values to represent interaction strength
    # print("interaction_matrix ",interaction_matrix)
    # Calculate user similarity using cosine similarity
    user_similarity = cosine_similarity(interaction_matrix)
    
    

    # Find similar users (excluding the target user)
    target_user_idx = users_list.index(Customer.objects.get(id=target_user_id))
    print("target_user_idx ",target_user_idx)
    
     # Get the target user's similarity vector
    target_user_similarity = user_similarity[target_user_id - 1]
    
    similar_users = target_user_similarity.argsort()[-num_recommendations-1:-1][::-1]
    print("similar_users ",similar_users)
    # similar_users = np.argsort(user_similarity[target_user_idx])[::-1][1:]  # Exclude target user
    # Exclude the current user
    exclusive_similar_users = [user_idx + 1 for user_idx in similar_users if user_idx + 1 != target_user_id]
    # exclusive_similar_users = [user_idx +1 for user_idx in similar_users if user_idx + 1 != target_user_id]
    print("exclusive_similar_users ",exclusive_similar_users)
    # Recommend products based on similar users' interactions
    recommended_products = []
    for user_idx in exclusive_similar_users:
        user_interaction = interaction_matrix[user_idx]
        new_recommendations = [products for product_idx, interaction_value in enumerate(user_interaction) if interaction_value == 1 and interaction_matrix[target_user_idx, product_idx] == 0]
        recommended_products.extend(new_recommendations)
        
    recommended_products = [product for queryset in recommended_products for product in queryset]

    # print("recommended_products ",recommended_products)
    return recommended_products[:5]  # Return the top 5 recommended products
