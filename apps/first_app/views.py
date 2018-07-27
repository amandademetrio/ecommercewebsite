from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages
import random

#Loading pages

def index(request):
    products = context = {
        'products':Product.objects.all(),
        'categories':Category.objects.all(),
        'clothing_n':Product.objects.filter(category_id=1).count(),
        'shoes_n':Product.objects.filter(category_id=2).count(),
        'acessories_n':Product.objects.filter(category_id=3).count()
    }
    return render(request,'first_app/index.html',context)

def loadadmin(request):
    if 'user_id' in request.session and request.session['logged_in'] == True:
        return redirect('/dashboard/orders')
    else:
        return render(request,'first_app/admin_index.html')

def loadproduct(request,number):
    product = Product.objects.get(id=number)
    clothing_products = Product.objects.filter(category_id=1).exclude(id=number)[:5]
    shoes_products = Product.objects.filter(category_id=2).exclude(id=number)[:5]
    a_products = Product.objects.filter(category_id=3).exclude(id=number)[:5]
    context = {
        'product': product,
        'clothing_products':clothing_products,
        'shoes_products':shoes_products,
        'a_products':a_products
    }
    return render(request,'first_app/productpage.html',context)

def loadcart(request):
    if 'current_order' in request.session and request.session['order_started'] == True:
        current_order = Order.objects.get(id=request.session['current_order'])
        context = {
            'order':current_order
        }
        return render(request,'first_app/cartpage.html',context)
    else:
        return render(request,'first_app/empty_cart_page.html')

def ordersuccess(request):
    if 'current_order' in request.session and 'checkout' in request.session and request.session['checkout'] == 'done':

        current_order = Order.objects.get(id=request.session['current_order'])
        context = {
            'order':current_order
        }
        request.session['order_started'] = False
        request.session['current_order'] = ''
        request.session['cart_count'] = 0
        return render(request,'first_app/ordersucess.html',context)
    else:
        return redirect('/')

def adminorders(request):
    if 'user_id' in request.session and request.session['logged_in'] == True:
        context = {
            'orders':Order.objects.all()
        }
        return render(request,'first_app/admin_orders.html',context)
    else:
        return redirect('/admin')

def adminproducts(request):
    if 'user_id' in request.session and request.session['logged_in'] == True:
        context = {
            'products':Product.objects.all()
        }
        return render(request,'first_app/admin_products.html',context)
    else:
        return redirect('/admin')

def adminoneorder(request,number):
    if 'user_id' in request.session and request.session['logged_in'] == True:
        order = Order.objects.get(id=number)
        subtotal = 0
        shipping_price = random.randrange(10)

        for product in order.products.all():
            subtotal += product.price

        total_price = subtotal + shipping_price

        context = {
            'order':order,
            'subtotal':subtotal,
            'shipping_price':shipping_price,
            'total_price':total_price
        }
        return render(request,'first_app/admin_orderpage.html',context)
    else:
        return redirect('/admin')

#Admin: working with DB

def find_product(request):
    products = Product.objects.filter(name__startswith=request.POST['search_product'])
    context = {
        'products':products
    }
    return render(request,'first_app/tables/product_table.html',context)

def find_order(request):
    if request.POST['search_order'] == '':
        orders = Order.objects.all()
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)
    elif request.POST['search_order'] != '':
        order = Order.objects.get(id=request.POST['search_order'])
        context = {
            'order':order
            }
        return render(request,'first_app/tables/order_table.html',context)

def add_product(request):
    if request.POST['new_cat'] == 'Clothing':
        new_p_category = Category.objects.get(id=1)
    elif request.POST['new_cat'] == 'Shoes':
        new_p_category = Category.objects.get(id=2)
    elif request.POST['new_cat'] == 'Acessories':
        new_p_category = Category.objects.get(id=3)

    Product.objects.create(name=request.POST['product_name'],main_picture=request.POST['product_picture'],description=request.POST['product_desc'],inventory_count=request.POST['inventory_count'],sold_count=0,price=request.POST['price'],category=new_p_category)
    return redirect('/dashboard/products')

def edit_product(request):
    product_to_edit = Product.objects.get(id=request.POST['product_id'])
    product_to_edit.name = request.POST['new_name']
    product_to_edit.main_picture = request.POST['new_picture']
    product_to_edit.description = request.POST['new_desc']
    product_to_edit.inventory_count = request.POST['new_inv_count']
    product_to_edit.sold_count = request.POST['new_sold']
    product_to_edit.price = request.POST['new_price']
    product_to_edit.save()
    return redirect('/dashboard/products')

def delete_product(request):    
    product_to_be_deleted = Product.objects.get(id=request.POST['product_id'])
    product_to_be_deleted.delete()
    return redirect('/dashboard/products')

def sort_order(request):
    if request.POST['sortedBy'] == 'Placed':
        order_status = OrderStatus.objects.get(id=1)
        orders = Order.objects.filter(order_status=order_status)
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)
    
    elif request.POST['sortedBy'] == 'Shipped':
        order_status = OrderStatus.objects.get(id=2)
        orders = Order.objects.filter(order_status=order_status)
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)
    
    elif request.POST['sortedBy'] == 'Cancelled':
        order_status = OrderStatus.objects.get(id=3)
        orders = Order.objects.filter(order_status=order_status)
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)
    
    elif request.POST['sortedBy'] == 'Delivered':
        order_status = OrderStatus.objects.get(id=4)
        orders = Order.objects.filter(order_status=order_status)
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)
    else:
        orders = Order.objects.all()
        context = {
            'orders':orders
        }
        return render(request,'first_app/tables/full_orders_table.html',context)

def change_status(request):
    order = Order.objects.get(id=request.POST['order_id'])
    if request.POST['new_order_status'] == 'Placed':
        new_status = OrderStatus.objects.get(id=1)

    elif request.POST['new_order_status'] == 'Shipped':
        new_status = OrderStatus.objects.get(id=2)

    elif request.POST['new_order_status'] == 'Cancelled':
        new_status = OrderStatus.objects.get(id=3)

    elif request.POST['new_order_status'] == 'Delivered':
        new_status = OrderStatus.objects.get(id=4)

    order.order_status = new_status
    order.save()

    return redirect(adminoneorder,number=order.id)

#User: searching DB

def user_product_find(request):
    products = Product.objects.filter(name__startswith=request.POST['product_search_name'])
    context = {
        'products':products
    }
    return render(request,'first_app/tables/front_page_products.html',context)

def user_product_find_cat(request):
    products = Product.objects.filter(category_id=request.POST['category']).filter(name__startswith=request.POST['product_search_name'])

    context = {
        'products':products
    }
    return render(request,'first_app/tables/front_page_products.html',context)

#Admin Registration/Login/Logout

def registration(request):
    errors = Admin.objects.basic_validator(request.POST)
    print(errors)

    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='registration_errors')
        return redirect('/admin')
    
    else:
        new_admin = Admin.objects.create(name=request.POST['full_name'],email=request.POST['email'],user_level=10,password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        new_admin.save()
        request.session['user_name'] = new_admin.name
        request.session['email'] = new_admin.email
        request.session['logged_in'] = True
        request.session['user_id'] = new_admin.id
        return redirect('/dashboard/orders')

def login(request):
    errors = Admin.objects.login_validator(request.POST)
    
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='login_errors')
        return redirect('/admin')
    
    else:
        login_user = Admin.objects.get(email=request.POST['email'])
        request.session['logged_in'] = True
        request.session['user_id'] = login_user.id
        return redirect('/dashboard/orders')

def logout(request):
    request.session.clear()
    return redirect('/admin')

#User: order creation, edit, etc

def add_to_cart(request):
    if 'order_started' in request.session and request.session['order_started'] == True:
        #add product to current order
        current_order = Order.objects.get(id=request.session['current_order'])

        product_to_add = Product.objects.get(id=request.POST['product_id'])

        current_order.products.add(product_to_add)

        request.session['cart_count'] = current_order.products.count()

        print(current_order.products.count())
        request.session['current_order'] = current_order.id

        return redirect("/")
    else:
        #Updating session:
        request.session['order_started'] = True

        order_status = OrderStatus.objects.get(id=5)
        shippment_price = 0
        payment_status = PaymentStatus.objects.get(id=3)
        customer = User.objects.create(full_name='no customer info yet',shipping_address='default',shipping_city='default',shipping_state='default',shipping_zipcode="00000",billing_address='default',billing_city='default',billing_state='DF',billing_zipcode="00000",user_level=0)

        #creating new order
        new_order = Order.objects.create(customer=customer,order_status=order_status,payment_status=payment_status,shippment_price=shippment_price)

        product_to_add = Product.objects.get(id=request.POST['product_id'])
        
        new_order.products.add(product_to_add)

        new_order.save()

        request.session['current_order'] = new_order.id
        
        request.session['cart_count'] = new_order.products.count()

        return redirect("/")

def submit_order(request):
    if 'order_started' in request.session and 'current_order' in request.session:
        #Validation
        errors = User.objects.address_validator(request.POST)

        if len(errors):
            for key,value in errors.items():
                messages.error(request,value)
                print(messages)
            return redirect('/loadcart')
        
        else:
            #Getting current order and customer associated with it
            order = Order.objects.get(id=request.session['current_order'])
            customer = User.objects.get(id=order.customer.id)

            customer.full_name = request.POST['full_name']
            customer.shipping_address = request.POST['address']
            customer.shipping_city = request.POST['city']
            customer.shipping_state = request.POST['state']
            customer.shipping_zipcode = request.POST['zipcode']

            if request.POST['billing_address'] != '':
                customer.billing_address = request.POST['billing_address']
                customer.billing_city = request.POST['billing_city']
                customer.billing_state = request.POST['billing_state']
                customer.billing_zipcode = request.POST['billing_zipcode']
            else:
                customer.billing_address = "Same as shipping"
                customer.billing_city = "Same as shipping"
                customer.billing_state = "Same as shipping"
                customer.billing_zipcode = "11111"

            customer.save()
            order.order_status = OrderStatus.objects.get(id=1)
            order.save()

            for item in order.products.all():
                if item.inventory_count > 0:
                    item.inventory_count -= 1
                    item.sold_count +=1
                    item.save()

            request.session['checkout'] = 'done'

            return redirect('/ordersuccess')

def cat_page(request,number):
    context = {
        'category':Category.objects.get(id=number),
        'products':Product.objects.filter(category_id=number)
    }
    return render(request,'first_app/cat_page.html',context)

def remove_from_cart(request):
    order_to_edit = Order.objects.get(id=request.POST['order_id'])
    order_to_edit_count = order_to_edit.products.count()

    if order_to_edit_count > 0:
        product_to_remove = Product.objects.get(id=request.POST['product_id'])
        order_to_edit.products.remove(product_to_remove)

        new_count = order_to_edit.products.count()
        print(new_count)
        if new_count == 0:
            request.session['order_started'] = False
            request.session['cart_count'] = 0
            request.session['current_order'] = ''

    return redirect('/loadcart')