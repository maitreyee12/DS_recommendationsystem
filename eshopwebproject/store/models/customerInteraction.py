from django.db import models
from store.models.customer import Customer
from store.models.product import Products

class CustomerInteractions(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=20)  # e.g., "purchase," "view," "like"
    # active = models.CharField(max_length=20)  # e.g., "0 : inactive & 1 as active"
    
    def saveInteraction(self):
        self.save()
    
    # @staticmethod
    # def get_customer_by_email(email):
    #     try:
    #         return Customer.objects.get(email=email)
    #     except:
    #         return False
    
    # def get_interaction_View(self):
    #     return CustomerInteractions.objects.filter(customer=self.customer,product=self.product,interaction_type="view")
    
    # def get_interactiondetails(self):
    #     return CustomerInteractions.objects.filter(customer=self.customer,product=self.product)
        
       
    # def isExists(self):
    #     if CustomerInteractions.objects.filter(customer=self.customer,product=self.product):
    #         return True
    #     return False
    
    # @staticmethod
    # def update_interaction(customerid,productid,type):
    #     interactionobj = CustomerInteractions.objects.get(customer=customerid,product=productid)
    #     interactionobj.interaction_type = type
    #     interactionobj.save()