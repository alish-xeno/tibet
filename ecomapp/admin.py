from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([
    Region, City, EcommerceAdmin, Customer, Subscriber,
    Category, WishList, ProductReview, Collection,
    OrganizationInformation, PaymentMethod, Quotation, QuotationReply, Cart, 
    CartProduct, Order, Payment, Slider,Blog, Message, Faq, BlogComment, Product, ProductImage
    ])

