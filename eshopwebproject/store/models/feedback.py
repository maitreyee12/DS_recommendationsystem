import datetime
from django.db import models
from store.models.orders import Order
from store.models.customer import Customer

from store.models.product import Products

class Feedback(models.Model):
    product_id= models.ForeignKey(Products, on_delete=models.CASCADE)
    order_id= models.ForeignKey(Order, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    ratings = models.IntegerField()
    date = models.DateField(default= datetime.datetime.today)
    
    # status = models.BooleanField (default=False)
    def saveRatings(self):
        self.save()
        
    @staticmethod
    def is_feedback_exists(f_id):
        if Feedback.objects.filter(id = f_id):
            return True
        return False
    
    @staticmethod
    def get_feedback_by_id(f_id):
        try:
            return Feedback.objects.get(id=f_id)
        except:
            return False
        
    @staticmethod
    def get_feedbacks_by_orderid(orderid):
        return Feedback.objects.filter(id=orderid)
    
    @staticmethod
    def update_feedback(feedbackid,ratings):
        feedbackobj = Feedback.objects.get(id=feedbackid)
        feedbackobj.ratings = ratings
        feedbackobj.save()