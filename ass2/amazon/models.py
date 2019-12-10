from django.db import models
from phone_field import PhoneField
# Create your models here.
class Shipment(models.Model):
    shipping_id = models.AutoField(primary_key = True,null = False)
    addr = models.CharField(max_length = 300)
    ship_date = models.DateField(null = True)
    method = models.CharField(max_length = 50)
    courier = models.CharField(max_length = 50)

    class Meta():
        db_table = 'Shipment'

class Payment(models.Model):
    payment_id = models.AutoField(primary_key = True,null = False)
    gift = models.CharField(max_length = 10,null = True)
    billing_addr = models.CharField(max_length = 300, default = '')
    paid_date = models.DateField(null = True)
    discount = models.IntegerField(null = True)
    card_num = models.IntegerField(default = 0)
    card_holder_name = models.CharField(max_length = 50, default = '')
    card_expr_date = models.DateField(default = '2019-01-01')

    class Meta():
        db_table = 'Payment'

class Order(models.Model):
    order_id = models.AutoField(primary_key = True, null = False)
    total_price = models.FloatField(default = 0.0)
    order_date = models.DateField(null = True)
    shipping = models.OneToOneField(Shipment, on_delete = models.CASCADE,default = 0)
    payment = models.OneToOneField(Payment,on_delete = models.CASCADE,default = 0)

    class Meta():
        db_table = 'Order'
        unique_together = (('order_id','shipping','payment'),)

class Member(models.Model):
    account_id = models.AutoField(primary_key= True,null = False)
    name = models.CharField(max_length = 100,default = '')
    email = models.CharField(max_length = 100,null = True)
    password = models.CharField (max_length = 20,default='')
    phone_num = models.CharField(max_length = 20,null =True)

    class Meta():
        db_table = 'Member'

class Friend(models.Model):
    account = models.ForeignKey(Member,on_delete = models.CASCADE,related_name = 'member',default = '')
    faccount = models.ForeignKey(Member,on_delete = models.CASCADE,related_name = 'friend',default = '')

    class Meta():
        db_table = 'Friend'
        unique_together =(('account','faccount'),)


class Buyer(Member):
    membership_stt = models.IntegerField(default = 0)
    order= models.ForeignKey(Order,on_delete = models.CASCADE,default = '')
    default_addr = models.CharField(max_length = 300,default = '')

    class Meta():
        db_table = 'Buyer'

class Buyer_optional_addr(models.Model):
    account = models.ForeignKey(Buyer,on_delete = models.CASCADE,default = '')
    optional_addr = models.CharField(max_length = 300,null = True)

    class Meta():
        db_table = 'Buyer_Optional_Addr'
        unique_together = (('account','optional_addr'),)

class Buyer_card(models.Model):
    card_number = models.CharField(max_length = 20,default = '')
    card_holder_name = models.CharField(max_length = 50, default = '')
    card_expr_date = models.DateField()
    account = models.ForeignKey(Buyer, on_delete = models.CASCADE, default = 0)

    class Meta():
        db_table = 'Buyer_Card'
        unique_together = (('account','card_number'),)

class Seller(Member):
    seller_phone_num = models.CharField(max_length = 20, default='')
    address = models.CharField(max_length = 300,default = '')
    country = models.CharField(max_length = 20,default = '')
    card_num = models.CharField(max_length = 20,default = '')
    card_expr_date = models.DateField(default = '2019-01-01')
    card_holder_name = models.CharField(max_length = 50,default = '')
    zip_code = models.CharField(max_length = 10,null = True)
    comp_name = models.CharField(max_length = 100,default = '')

    class Meta():
        db_table = 'Seller'

class Product(models.Model):
    product_id = models.AutoField(primary_key = True, null = False)
    stock = models.IntegerField(default = 1,null = False)
    descript = models.CharField(max_length = 500,default = '')
    product_name = models.CharField(max_length = 200,default = '')
    brand = models.CharField(max_length = 100,null = True)
    price = models.FloatField(default = 0.0)
    account = models.ForeignKey(Seller,on_delete = models.CASCADE,default = '')
    discount = models.IntegerField(null = True)
    order = models.ManyToManyField(Order,db_table = 'Includes',related_name = 'Order_ID')

    class Meta():
        db_table = 'Product'
    
class Refunds(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE,default = '')
    order = models.ForeignKey(Order,on_delete = models.CASCADE,default = '')
    account = models.ForeignKey(Buyer,on_delete = models.CASCADE,default = '')

    class Meta():
        db_table = 'Refunds'
        unique_together = (('order','product'),)

class Product_picture(models.Model):
    image = models.ImageField(null = True, upload_to = 'D:/University/3rd Year/DB/Ass/ass2/amazon/template/img/category')
    product = models.ForeignKey(Product,on_delete = models.CASCADE,default = 0)

    class Meta():
        db_table = 'Product_Picture'
        unique_together = (('product','image'),)

class Feature(models.Model):
    product = models.ForeignKey(Product,on_delete = models.CASCADE,default = 0)
    feature = models.CharField(max_length = 100, null = True)

    class Meta():
        db_table = 'Feature'
        unique_together = (('product','feature'),)

class Review(models.Model):
    review_id = models.AutoField(primary_key = True)
    cmt = models.CharField(max_length = 500, default = '')
    rating = models.IntegerField(null = True)
    account = models.ForeignKey(Buyer, on_delete = models.CASCADE, default = 0)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default = 0)

    class Meta():
        db_table = 'Review'

class Category(models.Model):
    category_id = models.AutoField(primary_key = True)
    category_name = models.CharField(max_length = 100, default = '')

    class Meta():
        db_table = 'Category'

class Subcategory(models.Model):
    subcategory_name = models.CharField(max_length = 100, default = '')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 0)
    contains = models.ManyToManyField(Product, db_table = 'Contains')

    class Meta():
        db_table = 'Subcategory'
        unique_together = (('subcategory_name','category'),)

class List(models.Model):
    list_name = models.AutoField(primary_key = True)
    privacy = models.BooleanField(default=True)
    list_type = models.IntegerField( default = 0)
    account = models.ForeignKey(Member, on_delete = models.CASCADE, default = 0)
    

    class Meta():
        db_table = 'List'
        unique_together = (('account','list_name'),)

class ConsistOf(models.Model):
    product = models.ForeignKey(Product,on_delete= models.CASCADE, default = 0)
    _list = models.ForeignKey(List,on_delete = models.CASCADE, default = 0)
    account_id = models.IntegerField(null = False, default = 0)
    quantity = models.IntegerField(default = 1)
    
    class Meta():
        db_table = 'ConsistOf'