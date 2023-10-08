from django.db import models
from .category import Category


class Products(models.Model):
    name= models.CharField(max_length=60)
    price= models.IntegerField(default=0)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default=1 )
    description= models.CharField(max_length=250, default='', blank=True, null= True)
    image= models.ImageField(upload_to='uploads/products/')
    features = models.TextField(max_length=250, default='',blank=True, null= True)
    
    @staticmethod
    def get_products_by_id(id):
        return Products.objects.filter(id=id)
    
    @staticmethod
    def get_products_by_idList(ids):
        return Products.objects.filter(id__in=ids)
    
    @staticmethod
    def get_all_products():
        return Products.objects.all()
    
    @staticmethod
    def remove_product_byid(self, id):
        self.cart[id]['quantity'] -= 1
        return Products.objects.filter(id=id).delete()
    
    @staticmethod
    def get_all_products_by_categoryid(cat_id):
        if cat_id:
            return Products.objects.filter(category=cat_id)
        else:
            return Products.get_all_products();
    
# def remove(self, product):
#     product_id = str(product.id)
#     if product_id in self.cart:
#         # Subtract 1 from the quantity
#         self.cart[product_id]['quantity'] -= 1
#         # If the quantity is now 0, then delete the item
#         if self.cart[product_id]['quantity'] == 0:
#             del self.cart[product_id]
#         self.save()
    