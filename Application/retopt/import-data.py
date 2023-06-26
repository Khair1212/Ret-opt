import os
import sys
import pandas as pd
from datetime import datetime
import django
import math

# Set up Django environment
sys.path.append('/home/nishad/Mine/Development/SPL-3/FinalProject/retopt/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retopt.settings')
django.setup()



from django.utils import timezone
from store.models import Product, Order, OrderItem, ShippingAdress
from segmentation.models import SegmentedCustomer
from account.models import Customer

# Replace 'your_app' with the actual name of the Django app containing your models.

# Customer.objects.all().delete()
# Product.objects.all().delete()
# Order.objects.all().delete()
# OrderItem.objects.all().delete()
SegmentedCustomer.objects.all().delete()

# def import_csv_data(csv_file_path):
#     with open(csv_file_path, 'r') as file:
#         df = pd.read_csv(csv_file_path)

#         # Convert date format
#         #df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d')

#         for index, row in df.iterrows():
#             # Extract data from CSV row
#             transaction_id = row['Transaction ID']
#             customer_id = row['Customer ID']
#             dob = row['DOB']
#             city_code = row['City Code']
#             gender = row['Gender']
#             transaction_date = row['Transaction Date']

#             if not math.isnan(row['Product Id']): 
#                 prod_subcat_code = (row['Prod Subcat Code'])
#                 prod_cat_code = (row['Prod Cat Code'])
#                 quantity = (row['Qty'])
#                 rate = float(row['Rate'])
#                 net_sales = float(row['Net_Sales'])
#                 product_id = row['Product Id']

#                 print(product_id)
#                 print(net_sales)

#             # Create or update the product category and subcategory IDs
#                 product, created = Product.objects.get_or_create(
#                     id=product_id,
#                     defaults={
#                         'name': '',  # Provide the product name as desired
#                         'product_cat': prod_cat_code,
#                         'product_sub_cat': prod_subcat_code,
#                         'price': rate
#                     }
#                 )
#             # Update other fields of the Product model as needed

#             # Create or update the order, order item, etc.
            
#             customer, _ = Customer.objects.get_or_create(
#                 id=customer_id,
#                 defaults={
#                     'DOB':dob,
#                     'gender':gender,
#                     'city_code':city_code
#                 }
#                 )

#             #print(product)
#             if not math.isnan(row['Product Id']):
#                 order = Order.objects.create(
#                     customer=customer,
#                     complete=False,
#                     transaction_id=transaction_id,
#                     date_ordered=transaction_date
#                 )
#                 order_item = OrderItem.objects.create(
#                     product=product,
#                     order=order,
#                     quantity=quantity
#                 )
#             # Update other fields of the Order and OrderItem models as needed

#         # Done importing data

#     print("CSV data imported successfully!")


# # Replace 'your_app.models' with the actual path to your models file.

# # Provide the path to your CSV file
# csv_file_path = '/Users/khair1212/Documents/Final Year Project/Ret-opt/archive/Processed Data/mergeed_transactions.csv'

# # Call the import function
# import_csv_data(csv_file_path)
