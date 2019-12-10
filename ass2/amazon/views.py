from django.shortcuts import render,get_object_or_404,redirect
from django.template import loader
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.views.decorators.csrf import csrf_protect,csrf_exempt 
from django.db.models import ImageField
from django.utils.datastructures import MultiValueDictKeyError

def homepage(request):
    return render(request = request,template_name='index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        email = request.POST['email']
        phone_number = request.POST['phone-number']

        try:
            check_username = Member.objects.get(name = username)
        except Member.DoesNotExist:
            newuser = Member(name =username,password = password,phone_num=phone_number,email=email)
            newuser.save()
            return redirect("amazon:login")

    return render(request=request,template_name='register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        try:
            check_user = Member.objects.get(name = username)
        except Member.DoesNotExist:
            return redirect("amazon:login")
        if check_user.password == password:
            request.session['id'] = check_user.account_id
            request.session['username'] = check_user.name
            return render(request = request, template_name='index.html',context = {'username' : request.session['username'] ,
            'id' : request.session['id'] })

    return render(request=request,template_name='login.html',context = {'id' : request.user.id})

def logout(request):
    return render(request = request, template_name='index.html')

def sell(request):
    try:
        check_seller = Seller.objects.get(pk = request.session['id'])
    except Seller.DoesNotExist:
        return redirect('amazon:register_seller')

    return redirect('amazon:sell_product')

def register_seller(request):
    if request.method == 'POST':
        account_id = request.session['id']
        phone_number = request.POST['phone-number']
        name = request.POST['full-name']
        address = request.POST['address-1'] + request.POST['address-2'] + request.POST['city'] + request.POST['province-state']
        country = request.POST['country']
        zip_code = request.POST['postal']
        card_holder = request.POST['card-holder']
        card_number = request.POST['card-number']
        card_expr_date = '20' + request.POST['year'] + '-' + request.POST['month'] + '-' +'01'
        company_name = request.POST['company_name']
        
        user = Member.objects.get(pk = account_id)
        newseller = Seller(pk = account_id, name = user.name, phone_num = user.phone_num, email = user.email, password = user.password,seller_phone_num=phone_number,address = address,country = country
        ,card_num = card_number,card_expr_date = card_expr_date,card_holder_name = card_holder,zip_code = zip_code,comp_name=company_name)
        newseller.save()

        return redirect('amazon:sell_product')

    return render(request = request,template_name='register_seller.html',context = {'username' : Member.objects.get(pk = request.session['id']).name ,
        'id'    : request.session['id']})

@csrf_exempt
def sell_product(request):
    if request.method == 'POST':
        product_name = request.POST['product-name']
        product_image = request.FILES['product-image']
        brand = request.POST['brand']
        price = request.POST['price']
        discount = request.POST['discount']
        stock = request.POST['stock']
        descript = request.POST['description']
        account_id = request.session['id']

        new_product = Product(product_name = product_name,stock = stock,descript = descript,brand = brand, price = price, discount = discount,account_id = request.session['id'])
        new_product.save()
        new_product_picture = Product_picture(image = product_image,product_id = new_product.product_id)
        new_product_picture.save()

        return render(request = request, template_name= 'index.html', context ={
            'username' : Member.objects.get(pk = request.session['id']).name,
            'id' : request.session['id']
        })

    return render(request = request,template_name= 'sell_product.html',context = {'username' : Member.objects.get(pk = request.session['id']).name ,
        'id'    : request.session['id']})

# def category(request):
#     product_list = Product.objects.order_by('product_id')
#     product_picture_list = Product_picture.objects.order_by('product_id')
#     return render(request = request, template_name= 'category.html', context= {
#         'product_list' : product_list,
#         'product_picture_list': product_picture_list,
#     })

def cart(request):
    payment = Payment()
    payment.save()
    shipment = Shipment()
    shipment.save()
    order = Order(payment_id = payment.payment_id, shipping_id = shipment.shipping_id)
    order.save()
    member = Member.objects.get(account_id = request.session['id'])
    buyer = Buyer(account_id = member.account_id,order_id = order.order_id, name = member.name, password = member.password,email = member.email, phone_num = member.phone_num )
    buyer.save()
    try:
        lproduct = List.objects.get(account_id = request.session['id'],list_type = 0)
    except List.DoesNotExist:
        lproduct = List(account_id = request.session['id'],list_type = 0)
        lproduct.save()

    # if request.method=="POST":
    #     p_id=request.POST['pr_id']
    #     input_num=request.POST['input_num']    
    #     product=Product.objects.get(product_id=p_id)
    #     addproduct=ConsistOf(product_id=product.product_id,_list_id=lproduct.list_name,account_id = lproduct.account_id,quantity =input_num)

    #     try:
    #         temp = ConsistOf.objects.get(product_id = product.product_id,_list_id = lproduct.list_name,account_id = lproduct.account_id)
    #     except ConsistOf.DoesNotExist:
    #         if input_num != addproduct.quantity:
    #             addproduct.quantity = input_num
    #         addproduct.save()
    #     #print(addproduct)
    # products=[]
    # product_pictures = []
    # lst = ConsistOf.objects.filter(_list_id = lproduct.list_name,account_id = request.session['id'])
    # for x in lst:
    #     products.append(Product.objects.get(product_id=x.product_id))
    #     product_pictures.append(Product_picture.objects.get(product_id = x.product_id))
    #     #print(products)

    # for x in product_pictures:
    #     x.image = str(x.image)[51:]

    # try:
    #     input_num = input_num
    # except UnboundLocalError:
    #     input_num = 1
    # infor = {
    #     'products': products,
    #     'input_num': input_num,
    #     'product_pictures': product_pictures,
    # }

    # return render(request,'cart.html', infor)
    
    if request.method=="POST":
        try:
            p_id=int(request.POST['pr_id'])
            input_num=int(request.POST['input_num'])
        except MultiValueDictKeyError:
            pass
    #lproduct=List.objects.get(account=1)
    #if p_id!=-1:
    product=Product.objects.get(product_id=p_id)
    addproduct=ConsistOf(product=product,_list=lproduct,quantity=input_num)
    addproduct.save()
    products=[]
    quantity=[]
    totalprice=[]
    for x in ConsistOf.objects.all():
        y=Product.objects.get(product_id=x.product_id)
        products.append(y)
        quantity.append(x.quantity)
        totalprice.append(x.quantity*y.price)
    infor = {
        'products': products,
        'quantity':quantity,
        'totalprice':totalprice,
    }
    return render(request,'cart.html', infor)


def single_product(request):
    if request.method=="POST":
        p_id=request.POST['s_product']
        product_picture = Product_picture.objects.get(product_id = p_id)
        product_picture.image = str(product_picture.image)[51:]

        infor = {
            'product': Product.objects.get(product_id=p_id),
            'product_picture': product_picture,
        }
    return render(request, 'single-product.html',infor)

def category(request):
    product_pictures = Product_picture.objects.all()
    for x in product_pictures:
        x.image = str(x.image)[51:]

    infor = {
        'products': Product.objects.all(),
        'product_pictures': product_pictures,
    }
    return render(request, 'category.html',infor)


def checkout_shipment(request):
    
    cart = List.objects.get(account_id = request.session['id'],list_type = 0)

    products_list = ConsistOf.objects.filter(_list_id = cart.list_name, account_id = request.session['id'])

    products = []
    for x in products_list:
        products.append(Product.objects.get(product_id = x.product_id))

    total = 0
    for x in products:
        total += ConsistOf.objects.get(_list_id = cart.list_name, account_id = request.session['id'], product_id = x.product_id).quantity*x.price
    infor = {
        'products': products,
        'products_list': products_list,
        'total': total,
    }
    return render(request,'checkout_shipment.html',infor)

def checkout_payment(request):
    if request.method == 'POST':
        buyer = Buyer.objects.get(account_id = request.session['id'])
        order = Order.objects.get(order_id = buyer.order_id)
        payment = Payment.objects.get(payment_id = order.payment_id)

        try:
            card_holer_name = request.POST['card-holder-name']
            card_num = request.POST['card-number']
            card_expr_date = '20' + request.POST['year'] + '-' + request.POST['month'] + '-01' 
        except MultiValueDictKeyError:
            pass
        
        try:
            payment.card_num = card_num
            payment.card_holder_name = card_holer_name
            payment.card_expr_date = card_expr_date
            payment.save()
            return redirect("amazon:confirmation")
        except UnboundLocalError:
            pass 
    
    cart = List.objects.get(account_id = request.session['id'],list_type = 0)

    products_list = ConsistOf.objects.filter(_list_id = cart.list_name, account_id = request.session['id'])

    products=[]
    quantity=[]
    for x in products_list:
        products.append(Product.objects.get(product_id=x.product_id))
        quantity.append(x.quantity)
    stotal=0
    for x in products:
        stotal += ConsistOf.objects.get(_list_id = cart.list_name, account_id = request.session['id'], product_id = x.product_id).quantity*x.price
    
    total=stotal+50
    
    infor={
        'products':products,
        'products_list': products_list,
        'quantity': quantity,
        'stotal':stotal,
        'total':total,
    }
    return render(request,'checkout_payment.html',infor)

def confirmation(request):
    cart = List.objects.get(account_id = request.session['id'],list_type = 0)

    products_list = ConsistOf.objects.filter(_list_id = cart.list_name, account_id = request.session['id'])

    products=[]
    for x in products_list:
        products.append(Product.objects.get(product_id=x.product_id))

    stotal=0
    for x in products:
        stotal += ConsistOf.objects.get(_list_id = cart.list_name, account_id = request.session['id'], product_id = x.product_id).quantity*x.price
    
    total=stotal+50
    
    infor={
        'products':products,
        'products_list': products_list,
        'stotal':stotal,
        'total':total,
    }
    return render(request,'confirmation.html',infor)

