from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import * 



#admin.site.register(Member)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Product)