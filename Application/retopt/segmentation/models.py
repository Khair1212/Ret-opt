from django.db import models

# Create your models here.
class Transactions(models.Model):
    transaction_id = models.IntegerField(primary_key=True)
    customer_id = models.IntegerField()
    transaction_date = models.DateField()
    product_subcat_code = models.IntegerField()
    product_cat_code = models.IntegerField()
    qty = models.IntegerField()
    rate = models.FloatField()
    tax = models.FloatField()
    total_amt = models.FloatField()
    store_type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.total_amt = self.qty * self.rate
        super(Transactions, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"Transaction {self.transaction_id} by Customer {self.customer_id}"


class Customer(models.Model):
    customer_Id = models.IntegerField(primary_key=True)
    DOB = models.DateField()
    Gender = models.CharField(max_length=1)
    city_code = models.DecimalField(max_digits=2, decimal_places=0)

    def __str__(self):
        return f"Customer {self.customer_Id}"

