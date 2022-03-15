from django.db import models
from django.contrib.auth.models import User, Group
from .constants import *
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.update_at = timezone.now()
        return super().save(*args, **kwargs)


class Region(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class City(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    default_shipping_charge = models.PositiveIntegerField(default=25)

    def __str__(self):
        return self.title


class EcommerceAdmin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="user/ecommerceadmin", null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        group, group_created = Group.objects.get_or_create(name="EcommerceAdmin")
        self.user.groups.add(group)
        super().save(*args, **kwargs)


class Customer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="user/customer", null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    
    def getFullName(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        group, group_create = Group.objects.get_or_create(name="Customer")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Subscriber(TimeStamp):
    email = models.EmailField()

    def __str__(self):
        return self.email


# productapp
class Category(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.ImageField(
        upload_to="category", null=True, blank=True)
    banner = models.ImageField(
        upload_to="category/banner/", null=True, blank=True)
    root = models.ForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True, verbose_name='On page ??')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('ecomapp:clientcategorydetail', kwargs ={
            'slug':self.slug
        })


class Product(TimeStamp):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    product_code = models.CharField(
        max_length=20, unique=True, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    display_image = models.ImageField(upload_to="products/products/")
    meta_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    return_policy = models.TextField(default="Can not be returned")
    warranty = models.CharField(max_length=300, default="No warranty")
    on_sale = models.BooleanField(default=False, null=True, blank=True)
    is_featured = models.BooleanField(default=False, null=True, blank=True)
    marked_price = models.DecimalField(max_digits=19, decimal_places=2)
    selling_price = models.DecimalField(max_digits=19, decimal_places=2)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecomapp:clientproductdetail", kwargs={"product_title": self.title, "slug":self.slug})
    
    

class ProductImage(TimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product/image/")
    
    def __str__(self):
        return f"{self.product} ({self.id})"


class WishList(TimeStamp):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="wproduct")

    def __str__(self):
        return self.customer.user.username


class ProductReview(TimeStamp):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    #if authenticated
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
    #if not 
    name = models.CharField(max_length=100, null = True, blank=True)
    email = models.EmailField(null = True, blank=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2)
    text = models.TextField()
    pros = models.TextField()
    cons = models.TextField()

    def __str__(self):
        return f"By: ({self.customer or self.email}) for ({self.product})."
    

class Collection(TimeStamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="collections")
    provide_discount = models.BooleanField(default=False)
    discount_pct = models.PositiveIntegerField(default=0)
    # end_date = models.DateField(null=True,blank=True)
    products = models.ManyToManyField(Product,blank=True)

    def __str__(self):
        return self.title

# ecommapp
class OrganizationInformation(TimeStamp):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="organization")
    profile_image = models.ImageField(upload_to="organization", null=True, blank=True)
    address = models.CharField(max_length=500)
    slogan = models.CharField(max_length=500, null=True, blank=True)
    contact_no = models.CharField(max_length=200)
    alt_contact_no = models.CharField(max_length=200, null=True, blank=True)
    map_location = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    alt_email = models.EmailField(null=True, blank=True)
    about_us = models.TextField()
    facebook = models.CharField(max_length=200,null=True,blank=True)
    instagram = models.CharField(max_length=200,null=True,blank=True)
    youtube = models.CharField(max_length=200,null=True,blank=True)
    twitter = models.CharField(max_length=200,null=True,blank=True)
    viber = models.CharField(max_length=200,null=True,blank=True)
    seller_policy = models.TextField()
    return_policy = models.TextField()
    support_policy = models.TextField()
    privacy_policy = models.TextField()
    terms_conditions = models.TextField()
    return_policy_for_products = models.TextField(null=True, blank=True)
    meta_description = models.CharField(max_length=256, null=True, blank=True)
    fb_messenger_script = models.CharField(
        max_length=1024, null=True, blank=True)
    google_analytics_script = models.CharField(
        max_length=500, null=True, blank=True)
    fb_pixel_script = models.CharField(max_length=4000, null=True, blank=True)
    detail_pixel = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Quotation(TimeStamp):
    name = models.CharField(max_length=200)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    email = models.EmailField()
    company = models.CharField(max_length=200, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    details = models.TextField()
    responded = models.BooleanField(default=False)

    def __str__(self):
    	return self.name + "(" + self.email + ")"
    

class QuotationReply(TimeStamp):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    message = models.TextField()
    attachment = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"Return to: {self.quotation.email}"


class PaymentMethod(TimeStamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='payment_methods')
    merchant_code = models.CharField(max_length=50, null=True, blank=True)
    test_secret_key = models.CharField(max_length=1024, null=True, blank=True)
    live_secret_key = models.CharField(max_length=1024, null=True, blank=True)
    test_public_key = models.CharField(max_length=1024, null=True, blank=True)
    live_public_key = models.CharField(max_length=1024, null=True, blank=True)
    client_js_url = models.TextField(null=True, blank=True)
    test_api_endpoint = models.CharField(max_length=200, null=True, blank=True)
    live_api_endpoint = models.CharField(max_length=200, null=True, blank=True)
    client_config_script = models.TextField(null=True, blank=True)
    payment_url = models.CharField(max_length=200, null=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Cart(TimeStamp):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    nettotal = models.DecimalField(max_digits=19, decimal_places=2)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "Cart: " + str(self.id)

    @property
    def total_shipping_charge(self):
        total = 0
        for cp in self.cartproduct_set.all():
            total += cp.shipping_charge
        return total

    @property
    def total_charge(self):
        total_charge = self.nettotal + self.total_shipping_charge
        return total_charge


class CartProduct(TimeStamp):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=19, decimal_places=2)
    subtotal = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_charge = models.PositiveIntegerField(default=50)
    order_status = models.CharField(
        max_length=200, choices=ORDER_STATUS, default='Pending')
    order_note = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return "Cart: " + str(self.cart.id) + " CartProduct: " + str(self.id)


class Order(TimeStamp):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    order_code = models.CharField(
        max_length=200, unique=True, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=19, decimal_places=2)
    discount = models.DecimalField(max_digits=19, decimal_places=2)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    shipping_charge = models.PositiveIntegerField(
        default=50, null=True, blank=True)
    shipping_charge_discount = models.PositiveIntegerField(
        default=0, null=True, blank=True)
    nettotal = models.DecimalField(max_digits=19, decimal_places=2)
    payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    customer_payment_status = models.BooleanField(default=False)
    requested_shipping_date = models.DateField(null=True, blank=True)
    is_guest_checkout = models.BooleanField(default=False)
    # billing address
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)
    street_address = models.CharField(max_length=200)
    is_complete = models.BooleanField(default=False)
    is_placed = models.BooleanField(default=False)
    placed_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    order_status = models.CharField(
        max_length=200, choices=ORDER_STATUS, default='Pending')
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return "Order: " + str(self.id)

        
class Payment(TimeStamp):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=19, decimal_places=2)
    tender = models.DecimalField(max_digits=19, decimal_places=2)
    change = models.DecimalField(max_digits=19, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.order.order_code


class Slider(TimeStamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="sliders")
    action_link_name = models.CharField(max_length=200, null=True, blank=True)
    action_link = models.CharField(max_length=200, null=True, blank=True)
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class Blog(TimeStamp):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to="blog", null=True, blank=True)
    content = models.TextField()
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(blank=True, null=True, unique=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True, null=True)
    is_featured = models.BooleanField(default=False, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug and self.title:
            self.slug = slugify(self.title, allow_unicode=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecomapp:clientblogdetail", kwargs={"slug": self.slug})
    


class BlogComment(TimeStamp):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    text = models.TextField(max_length=200)
    reply = models.ForeignKey("self", on_delete=models.CASCADE,
        null=True, blank=True, related_name="replies")

    def __str__(self):
        return f"By: ({self.user}) for ({self.blog})."


class Message(TimeStamp):
    name=models.CharField(max_length=200)
    email=models.EmailField()
    subject=models.CharField(max_length=500, null=True, blank=True)
    description=models.TextField()
    contact_no = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length = 200, null=True, blank=True)

    def __str__(self):
        return self.name


class Faq(TimeStamp):
    question = models.CharField(max_length=200)
    answer = models.TextField(max_length=200)

    def __str__(self):
        return self.question