import subprocess
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from account.models import Analyst
from store.models import Order
from segmentation.models import SegmentedCustomer
import csv, os
from pathlib import Path
from io import StringIO
from datetime import datetime
import sys
import os
import pandas as pd
import random
import io
import kaleido
from PIL import Image
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from segmentation.models import SegmentedCustomer, PlotImage
from store.models import Product, OrderItem
from account.models import Customer 
from segmentation.models import SegmentedCustomer
from django.http import JsonResponse


# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to the module search path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

# from .pre_process import receive

# Create your views here.


@user_passes_test(lambda u: u.is_authenticated and not u.is_customer)
def dashboard_view(request):
    if request.user.is_authenticated:
        # analyst = Analyst.objects.get(user=request.user)
        # print(analyst)
        return render(request, 'segmentation/dashboard.html',)


def segment_customer(request):
    if request.user.is_authenticated:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        process_model_path = os.path.join(BASE_DIR, "segmentation/process_model.py")
        subprocess.run(["python", process_model_path])
    
    return JsonResponse({'message': 'Processing code executed successfully'})

#@user_passes_test(lambda u: u.groups.filter(name='analyst').exists())
@user_passes_test(lambda u: u.is_authenticated and not u.is_customer)
def segmentation_view(request):
    

    
        
 #       return render(request, 'your_template.html', {'filtered_data': filtered_data, 'filtered': True})
 #   else:
        # Render the initial view with the button
 #       return render(request, 'your_template.html', {'filtered': False})

    if request.user.is_authenticated:
       
        name_filter = request.GET.get('name')
        segmented_customers = SegmentedCustomer.objects.all().order_by('-customer_id')
        # if name_filter:
        if request.method == 'GET' and 'name' in request.GET:
            segmented_customers = segmented_customers.filter(cluster_name__icontains=name_filter)
        
        if 'export' in request.GET:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="segmented_customers.csv"'

            writer = csv.writer(response)
            writer.writerow(['Customer ID', 'Name', 'Email', 'Cluster Name'])
            for customer in segmented_customers:
                writer.writerow([customer.customer_id, customer.name, customer.email, customer.cluster_name])

            return response

        paginator = Paginator(segmented_customers, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        plot_image = PlotImage.objects.get(id=1)

        context ={
            "customers": segmented_customers, 
            "plot_image": plot_image,
            "page_obj": page_obj,
        }
        return render(request, 'segmentation/analysis.html', context)


data_rows = []
def generate_dataframe():   
    orders = Order.objects.all()    
    for order in orders:    
        order_items = order.orderitem_set.all() 
        for item in order_items:    
            category_id = item.product.product_cat  
            sub_category_id = item.product.product_sub_cat  
            transaction_id = order.transaction_id   
            customer_id = order.customer.id 
            date = order.date_ordered.strftime('%m/%d/%y')  
            rate = item.product.price   
            quantity = item.quantity    
            net_sales = rate * quantity 

            data_rows.append([transaction_id, customer_id, date, sub_category_id, category_id, rate, quantity, net_sales]) 

    df = pd.DataFrame(data_rows, columns=['Transaction ID', 'Customer ID', 'Transaction Date', 'Prod Subcat Code', 'Prod Cat Code', 'Rate', 'Qty', 'Net_Sales'])
    
    #print(df[df['Customer ID'] == 275269]) 
    # print(df.shape)
    print("Dataframe is generated and transferred to the process_model file.")
    return df




def insert_processed_data(selected_columns, plot):
    
    # Save the plot as an image
    image_bytes = plot.to_image(format="png")
    image_file= io.BytesIO(image_bytes)
    
    # Create a PlotImage instance and save the image
    plot_image, created = PlotImage.objects.get_or_create(id=1)
    plot_image.image.save('plot_image.png', image_file, save=True)
    for index, row in selected_columns.iterrows():
        # Extract data from DataFrame row
        customer_id = row['Customer ID']
        cluster_name = row['Cluster_name']
        
        
        segmented_customer = SegmentedCustomer.objects.get_or_create(customer_id=customer_id, cluster_name=cluster_name)
    # print("Processed data is inserted.")

def generate_recommendation_dataframe():

    # Fetch data from models
    order_items = OrderItem.objects.select_related('product', 'order__customer').all()
    customers = Customer.objects.select_related('user').all()
    segmented_customers = SegmentedCustomer.objects.all()

    # Create lists to store data
    product_names = []
    product_codes = []
    quantities = []
    customer_ids = []
    customer_genders = []
    customer_ages = []
    city_codes = []
    cluster_names = []

    # Populate the lists with data
    for order_item in order_items:
        product_names.append(order_item.product.name)
        product_codes.append(order_item.product.id)
        quantities.append(order_item.quantity)
        customer_ids.append(order_item.order.customer.id)
        customer_genders.append(order_item.order.customer.gender)
        # customer_ages.append((pd.to_datetime('today').year - order_item.order.customer.DOB.year))
        customer_ages.append(random.randint(20, 30))
        city_codes.append(order_item.order.customer.city_code)


    # these are customers who have not ordered anything yet.     
    for customer in customers:  
        if customer.id in customer_ids: 
            continue  # Skip if already added through order_items   
        product_names.append('N/A')
        product_codes.append('N/A')
        quantities.append(0)
        customer_ids.append(customer.id)
        customer_genders.append(customer.gender)
        customer_ages.append((pd.to_datetime('today').year - customer.DOB.year))
        city_codes.append(customer.city_code)

    for segmented_customer in segmented_customers:
        cluster_names.append(segmented_customer.cluster_name)


     # Print the lengths of the arrays for debugging
    # print(len(product_names))
    # print(len(product_codes))
    # print(len(quantities))
    # print(len(customer_ids))
    # print(len(customer_genders))
    # print(len(customer_ages))
    # print(len(city_codes))
    # print(len(cluster_names))

    # Create DataFrame
    data = {
        'product_name': product_names,
        'product_code': product_codes,
        'quantity': quantities,
        'customer_id': customer_ids,
        'customer_gender': customer_genders,
        'customer_age': customer_ages,
        'city_code': city_codes,
        'cluster_name': cluster_names
    }
    df = pd.DataFrame(data)

    # print(df) 