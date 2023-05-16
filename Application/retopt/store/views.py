import datetime
from django.shortcuts import render

from account.models import Analyst
from .models import * 
from django.http import JsonResponse
import json 

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
# def create_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()  # Save the form data to the database
#             return HttpResponseRedirect('/products/')  # Redirect to a success page
#     else:
#         form = ProductForm()
#     return render(request, 'store/Store.html', {'form': form})




@login_required
def home(request):
    user = request.user
    print('User:', user)
    if user.is_authenticated:
        
        if user.is_customer==True:
            return redirect('store')
        elif user.is_analyst==True:
            return redirect('segmentation:clustering')
    else:
        return redirect('login')
    

@user_passes_test(lambda u: u.is_authenticated and not u.is_analyst)
def store(request):
    if request.user.is_authenticated :
        customer = Customer.objects.get(user=request.user)
        # print("Customer:",customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # print("Items:", items)
        cartItems = order.get_cart_items
        
    else:
        items = [] 
        order = {'get_cart_items':0, 'get_cart_total' : 0, 'shipping': False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    # print(Product.objects.latest('-id').image.url)
    context = {'products': products, 'cartItems': cartItems} 
    #context = {'products':products}   
    return render(request, 'store/Store.html', context)  


@user_passes_test(lambda u: u.is_authenticated and not u.is_analyst)
def cart(request):

    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        
    else:
        items = [] 
        order = {'get_cart_items':0, 'get_cart_total' : 0, 'shipping': False}
        cartItems = order['get_cart_items']
        

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/Cart.html', context) 


@user_passes_test(lambda u: u.is_authenticated and not u.is_analyst)
def checkout(request):
    if request.user.is_authenticated :
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = [] 
        order = {'get_cart_items':0, 'get_cart_total' : 0,  'shipping': False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'store/Checkout.html', context) 


@user_passes_test(lambda u: u.is_authenticated and not u.is_analyst)
def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print(action)
    print(productID)

    customer = request.user.customer
    product = Product.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item is added", safe=False)


#@user_passes_test(lambda u: u.groups.filter(name='customer').exists())
@csrf_exempt
@user_passes_test(lambda u: u.is_authenticated and not u.is_analyst)
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total==order.get_cart_total:
            order.complete=True
        order.save()

        if order.shipping == True:
            ShippingAdress.objects.create(
                customer=customer,
                order= order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode']
            )
    else:
        print('user is not logged in..')
    return JsonResponse('Purchase complete!', safe=False)