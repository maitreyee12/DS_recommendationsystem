from django.db import models
from .customer import Customer
from .product import Products

class Sessions(models.Model):
    custid= models.CharField(max_length=60)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    session_products= models.CharField(max_length=500)
    #session_products= models.C
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def saveSession(self):
        self.save()
        
    @staticmethod
    def is_session_exists(custid):
        if Sessions.objects.filter(custid = custid):
            return True
        return False
    
    @staticmethod
    def get_all_session_id(custid):
        sessionobj = Sessions.objects.filter(custid = custid)
        # print(sessionobj.objects.all()[0])
        #session_prods = Products.get_products_by_id(sessionobj.session_products)
        return sessionobj
    
    @staticmethod
    def update_session(self):
        sessionobj = Sessions.objects.get(custid=self.custid)
        sessionobj.session_products = self.session_products
        sessionobj.save()
    @staticmethod
    def remove_session(custid):
        return Sessions.objects.filter(custid=custid).delete()