from django.db import models
from django.conf import settings
from account.models import Customer
# Create your models here.


# class ProductCategory(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.id}"


# class ProductSubCategory(models.Model):
#     parent_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.id}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    product_cat = models.IntegerField(null=True, blank=True)
    product_sub_cat = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    # digital = models.BooleanField(default=False, null = True, blank = True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.id}'

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateField(default="2014-02-20")
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            shipping = True
        return shipping

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total

    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    def __str__(self) -> str:
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address


# class Transaction(models.Model):
#     transaction_id = models.CharField(max_length=100, null=True, primary_key=True)
#     cust_id = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True)
#     tran_date = models.DateTimeField(auto_now_add=True)
#     prod_cat_code = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_cat_code')
#     prod_subcat_code = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_subcat_code')
#     qty = models.IntegerField()
#     rate = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='price')
#     total_amt = models.FloatField()

#     def save(self, *args, **kwargs):
#         self.total_amt = self.qty * self.rate.price
#         super(Transaction, self).save(*args, **kwargs)
