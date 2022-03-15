from django.http.response import HttpResponse
from django.shortcuts import render, redirect, Http404
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import *
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum, Avg
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from itertools import chain
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from django.template.loader import render_to_string
from email.message import EmailMessage
from django.core.mail import EmailMessage


# Create your views here.

# HANDLERS
# HANDLERS
# HANDLERS
# HANDLERS


def handle404(request, exception=None):
    print(" handle 404 ++++++++++++++++++++++++++")
    return render(request, 'clienttemplates/404.html', {})


def handle500(request, *args, **argv):
    print(args, argv, 'handler500error')
    return render(request, 'clienttemplates/500.html', status=500)

#token generator
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return(
            six.text_type(user.pk) + six.text_type(login_timestamp) + six.text_type(timestamp)
        )

password_reset_token = TokenGenerator()

# Admin Views

class AdminRequiredMixin(SuccessMessageMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name="EcommerceAdmin").exists():
            pass
        else:
            return redirect('ecomapp:adminlogin')
        return super(AdminRequiredMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = OrganizationInformation.objects.first()
        context['pending_orders'] = Order.objects.filter(is_active=True, order_status="Pending")[:4]
        context['pending_order_count'] = Order.objects.filter(is_active=True, order_status="Pending").count()
        return context


class AdminLoginView(FormView):
    template_name = "admintemplates/adminlogin.html"
    form_class = AdminLoginForm
    success_url = reverse_lazy('ecomapp:adminhome')

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        pword = form.cleaned_data["password"]
        usr = authenticate(username=email, password=pword)
        if usr is not None:
            try:
                adminuser = usr.ecommerceadmin
                login(self.request, usr)
                messages.success(
                    self.request, f'Logged in as {usr.username} successfully.')
            except:
                messages.error(self.request, 'Invalid Email or Password')
                return render(self.request, self.template_name, {"error": "Invalid Email or Password", "form": form})
        else:
            messages.error(self.request, 'Invalid Email or Password')
            return render(self.request, self.template_name, {"error": "Invalid Email or Password", "form": form})
        return super().form_valid(form)

    def form_invalid(self, form):
        return super(AdminLoginView, self).form_invalid(form)

    # def get_success_url(self):
    #     if 'next' in self.request.GET:
    #         return self.request.GET.get('next')
    #     else:
    #         return self.success_url

class AdminLogoutView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect('ecomapp:adminlogin')
        else:
            raise Http404

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "admintemplates/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['customercount'] = Customer.objects.filter(is_active=True).count()
        context['productcount'] = Product.objects.filter(is_active=True).count()
        context['ordercount'] = Order.objects.filter(is_active=True).count()
        context['quotationcount'] = Quotation.objects.filter(is_active=True).count()
        context['messagecount'] = Message.objects.filter(is_active=True).count()
        context['subscribercount'] = Subscriber.objects.filter(is_active=True).count()
        context['latestorder'] = Order.objects.order_by('-created_at')[0:7]
        return context


class AdminOrganizationDetailView(AdminRequiredMixin, TemplateView):
    template_name = "admintemplates/adminorganizationdetail.html"


class AdminOrganizationUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminorganizationupdate.html"
    model = OrganizationInformation
    form_class = OrganizationForm
    success_url = reverse_lazy('ecomapp:adminorganizationdetail')
    
    def form_invalid(self, form):
        print("error")
        return super().form_invalid(form)


class AdminCustomerListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/admincustomerlist.html"
    queryset = Customer.objects.all()
    context_object_name = "customerlist"
    paginate_by = "20"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            customer = Customer.objects.get(id=self.request.GET.get('id'))
            customer.delete()

        return context

class AdminEcomAdminList(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminecomadminlist.html"
    queryset = EcommerceAdmin.objects.all()
    context_object_name = "ecomadminlist"
    paginate_by = "20"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            ecomadmin = EcommerceAdmin.objects.get(id=self.request.GET.get('id'))
            ecomadmin.delete()

        return context    


# Admin Product Category Views
class AdminCategoryListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminproductcategorylist.html"
    queryset = Category.objects.all()
    context_object_name = "categorylist"
    paginate_by = "10"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            category = Category.objects.get(id=self.request.GET.get('id'))
            category.delete()

        return context

class AdminCategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/admincategorycreate.html"
    form_class = AdminCategoryForm
    success_url = reverse_lazy('ecomapp:admincategorylist')


class AdminCategoryUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/admincategorycreate.html"
    model = Category
    form_class = AdminCategoryForm
    success_url = reverse_lazy('ecomapp:admincategorylist')


# Admin Product Views
class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminproductlist.html"
    queryset = Product.objects.all()
    context_object_name = "productlist"
    paginate_by = "25"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            product = Product.objects.get(id=self.request.GET.get('id'))
            product.delete()

        return context

class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/adminproductcreate.html"
    form_class = AdminProductForm
    success_url = reverse_lazy('ecomapp:adminproductlist')


class AdminProductUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminproductcreate.html"
    model = Product
    form_class = AdminProductForm
    success_url = reverse_lazy('ecomapp:adminproductlist')

    def get_success_url(self):
        return reverse('ecomapp:adminproductdetail', kwargs={
            'pk': self.kwargs['pk'],
        })


class AdminProductDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminproductdetail.html"
    model = Product
    context_object_name = "productobject"


# Admin Product Image Management
class AdminProductImageManageView(AdminRequiredMixin, TemplateView):
    template_name = "admintemplates/adminproductimagemanage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['pk'])
        context['productobject'] = product
        if self.request.is_ajax():
            img_id = self.request.GET.get('img_id')
            if img_id:
                pimage = ProductImage.objects.get(id=img_id).delete()

        return context

    def post(self, request, **kwargs):
        try:
            image = request.FILES['image']
            pimage = request.POST['productimage']
            product = Product.objects.get(id=self.kwargs['pk'])
            if pimage == "productimage":
                product_image = ProductImage.objects.create(product=product,image=image)
            elif pimage == "display_image":
                product.display_image = image
                product.save()
            return JsonResponse({'message': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'error'})


# Admin Order Views
class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminorderlist.html"
    queryset = Order.objects.all()
    context_object_name = "orderlist"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('status'):
            if self.request.GET.get('status') == 'allorders':
                orderlist = Order.objects.all()
            else:
                orderlist = Order.objects.filter(order_status=self.request.GET.get('status'))
        else:
            orderlist = Order.objects.filter(order_status='Pending')
        context['status'] = self.request.GET.get('status', 'pending')
        if self.request.is_ajax():
            order = Order.objects.get(id=self.request.GET.get('id'))
            order.delete()

        page = self.request.GET.get('page', 1)
        paginator = Paginator(orderlist, 25)
        try:
            updates = paginator.page(page)
        except PageNotAnInteger:
            updates = paginator.page(1)
        except EmptyPage:
            updates = paginator.page(paginator.num_pages)
        context['ordercount'] = orderlist.count()
        context['orderlist'] = updates

        context['allorderscount'] = Order.objects.all().count()
        context['pendingorderscount'] = Order.objects.filter(order_status='Pending').count()
        context['processingorderscount'] = Order.objects.filter(order_status='Order Processing').count()
        context['intransitorderscount'] = Order.objects.filter(order_status='OnTheWay').count()
        context['deliveredorderscount'] = Order.objects.filter(order_status='Delivered').count()
        context['canceledorderscount'] = Order.objects.filter(order_status='Canceled').count()
        return context


class AdminOrderUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminordercreate.html"
    model = Order
    form_class = AdminOrderForm
    success_url = reverse_lazy('ecomapp:adminorderlist')
    success_message = "Oreder Updated Sucessfully"


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminorderdetail.html"
    model = Order
    context_object_name = "orderobject"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=self.kwargs['pk'])
        try:
            if self.request.is_ajax():
                status = self.request.GET.get('status')
                if status == "Delivered":
                    order.is_complete = True
                else:
                    order.is_complete = False
                order.order_status = status
                order.save()
                print('success')
        except Exception as e:
            print(e)

        return context


class AdminCustomerDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/admincustomerdetail.html"
    model = Customer
    context_object_name = "customerobject"


class AdminCustomerUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/admincustomerupdate.html"
    model = Customer
    form_class = AdminCustomerForm
    success_url = reverse_lazy("ecomapp:admincustomerlist")
    success_message = "Customer Updated Sucessfully"

#admin sliders
class AdminSliderListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminsliderlist.html"
    queryset = Slider.objects.all()
    context_object_name = "sliderobj"
    paginate_by = "10"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            slider = Slider.objects.get(id=self.request.GET.get('id'))
            slider.delete()
        return context
    

class AdminSliderDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminsliderdetail.html"
    model = Slider
    context_object_name = 'sliderobject'

class AdminSliderCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/adminslidercreate.html"
    form_class = SliderCreateForm
    success_url = reverse_lazy("ecomapp:adminsliderlist")
    success_message = "Slider Created Sucessfully"

class AdminSliderUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminslidercreate.html"
    model = Slider
    form_class = SliderCreateForm
    success_url = reverse_lazy("ecomapp:adminsliderlist")
    success_message = "Slider Updated Sucessfully"

#admin-blog
class AdminBlogListView(AdminRequiredMixin,ListView):
    template_name = "admintemplates/adminbloglist.html"
    queryset = Blog.objects.all()
    context_object_name = 'blogobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            blog = Blog.objects.get(id=self.request.GET.get('id'))
            blog.delete()
        return context

class AdminBlogCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/adminblogcreate.html"
    form_class = AdminBlogForm
    success_url = reverse_lazy('ecomapp:adminbloglist')
    success_message = "Blog Created Sucessfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class AdminBlogUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminblogcreate.html"
    model = Blog
    form_class = AdminBlogForm
    success_url = reverse_lazy('ecomapp:adminbloglist')
    success_message = "Blog Updated Sucessfully"

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     form.save()
    #     return super().form_valid(form)

class AdminBlogDetailView(AdminRequiredMixin, DetailView):
    template_name = 'admintemplates/adminblogdetail.html'
    model = Blog
    context_object_name = "adminblogdetail"

#admin region
class AdminRegionListView(AdminRequiredMixin, ListView):
    template_name = "admintemplates/adminregionlist.html"
    queryset = Region.objects.all()
    context_object_name = 'regionobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            region = Region.objects.get(id=self.request.GET.get('id'))
            region.delete()
        return context    

class AdminRegionUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/adminregionupdate.html'
    model = Region
    form_class = AdminRegionForm
    success_url = reverse_lazy("ecomapp:adminregionlist")
    success_message = "Region Updated Sucessfully"

class AdminRegionCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admintemplates/adminregionupdate.html'
    model = Region
    form_class = AdminRegionForm
    success_url = reverse_lazy("ecomapp:adminregionlist")
    success_message = "Region Created Sucessfully"

#admin city
class AdminCityListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/admincitylist.html'
    queryset = City.objects.all()
    context_object_name = 'cityobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            city = City.objects.get(id=self.request.GET.get('id'))
            city.delete()
        return context

class AdminCityUpdateView(AdminRequiredMixin, UpdateView):
    template_name = 'admintemplates/admincityupdate.html'
    model = City
    form_class = AdminCityForm
    success_url = reverse_lazy("ecomapp:admincitylist")
    success_message = "City Updated Sucessfully"

class AdminCityCreateView(AdminRequiredMixin, CreateView):
    template_name = 'admintemplates/admincityupdate.html'
    model = City
    form_class = AdminCityForm
    success_url = reverse_lazy("ecomapp:admincitylist")
    success_message = "City Created Sucessfully"

# admin faq
class AdminFAQListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminfaqlist.html'
    queryset = Faq.objects.all()
    context_object_name = 'faqobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            faq = Faq.objects.get(id=self.request.GET.get('id'))
            faq.delete()
        return context

class AdminFAQDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminfaqdetail.html"
    model = Faq
    context_object_name = "adminfaqdetailobj"

class AdminFAQCreateView(AdminRequiredMixin, CreateView):
    template_name = "admintemplates/adminfaqcreate.html"
    form_class = AdminFaqForm
    model = Faq
    success_url = reverse_lazy("ecomapp:adminfaqlist")
    success_message = "FAQ Created Sucessfully"

class AdminFAQUpdateView(AdminRequiredMixin, UpdateView):
    template_name = "admintemplates/adminfaqcreate.html"
    form_class = AdminFaqForm
    model = Faq
    success_url = reverse_lazy("ecomapp:adminfaqlist")
    success_message = "FAQ Updated Sucessfully"

#admin suscribers
class AdminSuscriberListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminsuscriberlist.html'
    queryset = Subscriber.objects.all()
    context_object_name = 'subobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            sub = Subscriber.objects.get(id=self.request.GET.get('id'))
            sub.delete()
        return context

#admin Quotation:
class AdminQuotationListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminquotationlist.html'
    queryset = Quotation.objects.all()
    context_object_name = 'quotobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            quot = Quotation.objects.get(id=self.request.GET.get('id'))
            quot.delete()
        return context

class AdminQuotationDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminquotationdetail.html"
    model = Quotation
    context_object_name = "quotationobj"

class AdminMessageListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminmessagelist.html'
    queryset = Message.objects.all().order_by('-id')
    context_object_name = 'msgobj'
    paginate_by = '10'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.is_ajax():
            msg = Message.objects.get(id=self.request.GET.get('id'))
            msg.delete()
        return context

class AdminMessageDetailView(AdminRequiredMixin, DetailView):
    template_name = "admintemplates/adminmessagedetail.html"
    model = Message
    context_object_name = "msgonj"


# Client Views
class ClientMixin(SuccessMessageMixin, object):
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['org'] = OrganizationInformation.objects.last()
        context['rootcategory'] = Category.objects.filter(root = None)
        user = self.request.user
        if user.is_authenticated and user.groups.filter(name="Customer").exists():
            context["wishlist"] = WishList.objects.filter(customer = user.customer).last()
        cart_id = self.request.session.get('mycart', None)
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                try:
                    order = cart.order
                    if order.is_complete or (order.order_status == "Canceled" and order.payment_method is None):
                        del self.request.session['mycart']
                except:
                    if user.is_authenticated and user.groups.filter(name="Customer").exists():
                        if cart.customer is None:
                            cart.customer = Customer.objects.get(user=user)
                            cart.save()
                        context['customer'] = cart.customer
            except Exception as e:
                print(e)
                cart = None
        elif user.is_authenticated and user.groups.filter(
                name="Customer").exists():
            customer = Customer.objects.get(user=user)
            context['customer'] = customer
            last_cart = Cart.objects.filter(
                customer=customer, order__is_complete=False).last()
            cart = last_cart
            if cart:
                self.request.session['mycart'] = cart.id
            else:
                self.request.session['mycart'] = None
        else:
            cart = None

        context['cart'] = cart
        return context


class ClientHomeView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clienthome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["sliderlist"] = Slider.objects.all().order_by("-id")[:3]
            context['latestbloglist'] = Blog.objects.all().order_by("-id")[:10]
            context['featuredblogs'] = Blog.objects.filter(is_featured=True).order_by("-id")[:3]
            context["bestseller"] = Product.objects.all().order_by('-id')[:4]
            context["collectionlist"] = Collection.objects.all().order_by("-id")[:3]
            # collectionlist = Collection.objects.all().order_by("-id")
            productlist = Product.objects.all().order_by('-id')[:8]
            
            # for product in productlist:
            #     for collection in collectionlist:s
            #         # print(collection)
            #         if product in collection.products.all:
            #             print("sale")
            #         else:
            #             print("no sale")

            # page = self.request.GET.get('page', 1)
            # paginator = Paginator(productlist, 20)
            # try:
            #     updates = paginator.page(page)
            # except PageNotAnInteger:
            #     updates = paginator.page(1)
            # except EmptyPage:
            #     updates = paginator.page(paginator.num_pages)
            context['productlist'] = productlist
            context["onsalepdocutlist"] = Product.objects.filter(on_sale = True).order_by("-id")[:10]
        except Exception as e:
            print(e, 'clienthome error')
        return context


class ClientAddToWishlist(ClientMixin, View):
    def post(self, request):
        try:
            product_obj = Product.objects.get(id = self.request.POST["product_id"])
            # print(product_obj,"------------------------------")
            wishlist = WishList.objects.filter(customer = self.request.user.customer).last()
            # print(wishlist,"++++++++++++++++++++++++")
            # if wishlist is None:
            #     wishlist = WishList.objects.create(customer = self.request.user.customer)
            #     print(wishlist)
            if product_obj in wishlist.products.all():
                wishlist.products.remove(self.request.POST["product_id"])
                count = wishlist.products.all().count()
                return JsonResponse({"message":"removed", 'product_obj': product_obj.title})

            else:
                wishlist.products.add(self.request.POST["product_id"])
                count = wishlist.products.all().count()
                return JsonResponse({"message":"added", 'product_obj': product_obj.title})
        except Exception as e:
            print(e, 'homeview mixin')
            return JsonResponse({"message":"error"})
        return JsonResponse({"count":count})

class ClientLoginView(ClientMixin, FormView):
    template_name = "clienttemplates/clientlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy('ecomapp:clienthome')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        pword = form.cleaned_data['password']
        usr = authenticate(username=email, password=pword)
        if usr is not None:
            print('hhhhhhhhhh')
        try:
            print('try')
            customer = usr.customer
            login(self.request, usr)
            messages.success(self.request, "Logged in successfully.")
        except Exception as e:
            print(e, '\n loginerror')
            messages.error(self.request, 'Invalid Email or Password')
            return render(self.request, self.template_name, {"error": "Invalid Email or Password", "form": form})

        # else:
        #     messages.error(self.request, 'some errors')
        #     return render(self.request, self.template_name,
        #                 {"error": "Invalid username or password", "form": form})

        return super().form_valid(form)

    def form_invalid(self, form):
        print("Invalid")
        return super().form_invalid(form)

    def get_success_url(self):
        if self.request.GET:
            next_url = self.request.GET['next']
            return next_url
        else:
            return self.success_url

class ClientLogoutView(View):
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(self.request, "Logged out successfully.")
            return redirect('ecomapp:clienthome')
        else:
            raise Http404


class ClientAllProducts(ClientMixin, ListView):
    template_name = "clienttemplates/clientallproducts.html"
    queryset = Product.objects.all()
    context_object_name = 'allproducts'
    paginate_by = '20'


class ClientProductDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientproductdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            product = Product.objects.get(slug=self.kwargs['slug'])
            context['product'] = product
            context["reviewlist"] = ProductReview.objects.filter(product=product).order_by("-id")[:5]
            context["productlist"] = Product.objects.all().order_by('-id')
            totalreview = ProductReview.objects.filter(product = product).count()
            context["totalreview"] = totalreview
            recomendreview = ProductReview.objects.filter(product = product, rating__in = [4,5]).count()
            context['recomendreview'] = recomendreview
            if totalreview != 0:
                context["recomendreviewpct"] = (recomendreview / totalreview) * 100
            context["reviewaverage"] = ProductReview.objects.filter(product = product).aggregate(Avg("rating"))["rating__avg"]
            context["star_5"] = ProductReview.objects.filter(product = product, rating = 5.00).count()
            context["star_4"] = ProductReview.objects.filter(product = product, rating = 4.00).count()
            context["star_3"] = ProductReview.objects.filter(product = product, rating = 3.00).count()
            context["star_2"] = ProductReview.objects.filter(product = product, rating = 2.00).count()
            context["star_1"] = ProductReview.objects.filter(product = product, rating = 1.00).count()
            # avg = ProductReview.objects.filter(product = product).aggregate(Avg("rating"))["rating__avg"]
            # print(avg)
        except Exception as e:
            print(e, "ClientProductDetailView")
            context['product'] = 'none'
        return context
    
    def post(self, request, *args, **kwargs):
        product_obj = Product.objects.get(slug = self.kwargs["slug"])
        rating = self.request.POST['rating']
        text = self.request.POST['text']
        pros = self.request.POST['pros']
        cons = self.request.POST['cons']
        print(product_obj)
        if self.request.user.is_authenticated:
            if ProductReview.objects.filter(product=product_obj, customer = self.request.user.customer).exists():
                return JsonResponse({"message":"customererror"})
            else:
                ProductReview.objects.create(product=product_obj, customer = self.request.user.customer, rating = rating, text=text,pros=pros,cons=cons)
                return JsonResponse({"message":"customersuccess"})
        else:
            if ProductReview.objects.filter(product=product_obj, email=self.request.POST['email']):
                return JsonResponse({"message":"guesterror"})
            else:
                ProductReview.objects.create(product=product_obj, name = self.request.POST['name'], email=self.request.POST['email'], rating = rating, text=text,pros=pros,cons=cons)
                return JsonResponse({"message":"guestsuccess"})


class ClientCartDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientcartdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ClientCheckoutView(ClientMixin, FormView):
    template_name = "clienttemplates/clientcheckout.html"
    form_class = ClientOrderForm
    success_url = reverse_lazy("ecomapp:clientcheckoutpayment")

    def dispatch(self, request):
        cart_id = self.request.session.get('mycart', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            if cart.cartproduct_set.count() > 0:
                self.order = Order.objects.filter(cart=cart).first()
                if self.order and request.META.get('HTTP_REFERER') is None:
                    self.order.discount = 0
                    self.order.total = self.order.subtotal
                    self.order.nettotal = self.order.total + self.order.shipping_charge
                    self.order.save()
                    return redirect('ecomapp:clientcart')
                if (self.order is not None and self.order.is_complete is False):
                    return redirect('ecomapp:clientorderupdate', pk=cart.order.id)
            else:
                return redirect('ecomapp:clienthome')
        else:
            return redirect('ecomapp:clienthome')
        return super().dispatch(request)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all().order_by('title')
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('mycart', None)
        cart = Cart.objects.get(id=cart_id)
        cart_order = Order.objects.filter(cart=cart).first()
        region = Region.objects.filter(
            slug=self.request.POST.get('region')).last()
        form.instance.region = region
        form.instance.city = City.objects.filter(
            slug=self.request.POST.get('city')).last()

        if cart_order:
            return redirect('ecommapp:clientorderupdate', pk=cart_order.id)
        else:
            order = form.save(commit=False)
            shipping_charge = 0
            for cp in cart.cartproduct_set.all():
                shipping_charge += cp.shipping_charge
            order.shipping_charge = shipping_charge
            order.cart = cart
            order.discount = 0
            order.subtotal = cart.nettotal
            order.total = order.subtotal - order.discount
            order.nettotal = order.total + order.shipping_charge
            order.save()
            order.order_code = 'order_' + str(order.id)
            order.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)


class ClientOrderUpdateView(ClientMixin, UpdateView):
    template_name = "clienttemplates/clientcheckout.html"
    model = Order
    form_class = ClientOrderForm
    success_url = reverse_lazy("ecomapp:clientcheckoutpayment")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('mycart', None)
        cart = Cart.objects.get(id=cart_id)
        cart_order = Order.objects.filter(cart=cart).first()

        context['regions'] = Region.objects.all().order_by('title')
        if cart_order.city:
            region = cart_order.city.region
            context['cities'] = City.objects.filter(region=region).order_by('title')

        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('mycart', None)
        cart = Cart.objects.get(id=cart_id)
        cart_order = Order.objects.filter(cart=cart).first()
        region = Region.objects.filter(slug=self.request.POST.get('region')).last()
        if region:
            form.instance.region = region
        else:
            form.instance.region = None

        city = City.objects.filter(slug=self.request.POST.get('city')).last()
        if city:
            form.instance.city = city
        else:
            form.instance.city = None

        order = form.save(commit=False)
        shipping_charge = 0
        for cp in cart.cartproduct_set.all():
            shipping_charge += cp.shipping_charge
        order.shipping_charge = shipping_charge
        order.cart = cart
        order.discount = 0
        order.subtotal = cart.nettotal
        order.total = order.subtotal - order.discount
        order.nettotal = order.total + order.shipping_charge
        order.save()
        order.order_code = 'order_' + str(order.id)
        order.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        print('invalid')
        return super().form_invalid(form)

class ClientOrederDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientorderdetail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id = self.kwargs['pk'])
        context["cartproduct"] = CartProduct.objects.filter(cart = order.cart)
        # print(cartproduct.product)
        context["orderdetail"] = Order.objects.get(id = self.kwargs['pk']) 
        return context


class ClientCheckoutPaymentView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientcheckoutpayment.html"


class ClientCheckoutReviewView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientcheckoutreview.html"

    def post(self, request, *args, **kwargs):
        today = timezone.localtime(timezone.now())
        cart_id = self.request.session.get('mycart', None)
        cart = Cart.objects.get(id=cart_id)
        cart_order = Order.objects.filter(cart=cart).first()
        cart_order.is_placed = True
        cart_order.placed_date = today
        cart_order.save()
        email = cart_order.email
        html_template = "clienttemplates/order_conf.html"
        print("******************************")
        html_message  = render_to_string(html_template)
        message = EmailMessage(
            'subject',
            html_message,
            settings.EMAIL_HOST_USER,
            (email, )
        )
        message.content_subtype = 'html'
        message.send()
        print("*******we have send you mail*****")
        # send_mail(
        #     'subject',
        #     text_content + html_content,
        #     settings.EMAIL_HOST_USER,
        #     (email, ),
        #     fail_silently=False,
        # )

        del request.session['mycart']

        return JsonResponse({"message": 'success'})


class ClientCheckoutCompleteView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientcheckoutcomplete.html"

    def dispatch(self, request):
        cart_id = self.request.session.get('mycart', None)
        if cart_id:
            return redirect('ecomapp:clienthome')
        return super().dispatch(request)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     order = Order.objects.filter(id=self.kwargs['pk']).last()

    #     return context

class ClientCategoryDetailView(ClientMixin, TemplateView):
    template_name = 'clienttemplates/clientcategorydetail.html'
    # model = Category
    # context_object_name = 'categorydetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_by = self.request.GET.get('sorting')
        try:
            category = Category.objects.get(slug=self.kwargs['slug'])
            context['category'] = category.slug
            if category.root:
                productlist = Product.objects.filter(category=category).order_by('id')
                context['superroot'] = category.root
                context['count'] = productlist.count()
            else:
                subcategory = Category.objects.filter(root=category)
                productlist = list(chain(Product.objects.filter(category__in=subcategory).order_by('id'), Product.objects.filter(category=category).order_by('id')))
                context['count'] = len(productlist)
            # if self.request.user.is_authenticated:
                # context['wishlist'] = WishList.objects.get(customer=self.request.user.customer)
            try:
                if sort_by:
                    if sort_by == 'lf_order':
                        productlist = productlist.order_by('-id')
                    elif sort_by == 'of_order':
                        productlist = productlist.order_by('id')
                    elif sort_by == 'lh_order':
                        productlist = productlist.order_by('selling_price')
                    elif sort_by == 'hl_order':
                        productlist = productlist.order_by('-selling_price')
                    elif sort_by == 'ar_order':
                        productlist = productlist.order_by('selling_price')
                    elif sort_by == 'az_order':
                        productlist = productlist.order_by(Lower('title'))
                    elif sort_by == 'za_order':
                        productlist = productlist.order_by(Lower('title').desc())
                    else:
                        productlist = productlist.order_by('-id')
                    context['sorting'] = sort_by
                else:
                    context['sorting'] = 'lf_order'
                    productlist = productlist.order_by('-id')
            except Exception as e:
                print(e, 'ClientCategoryDetailView sorting error')
                if sort_by:
                    if sort_by == 'lf_order':
                        productlist = sorted(productlist, key=lambda x: x.id, reverse=True)
                    elif sort_by == 'of_order':
                        productlist = sorted(productlist, key=lambda x: x.id, reverse=False)
                    elif sort_by == 'lh_order':
                        productlist = sorted(productlist, key=lambda x: x.selling_price, reverse=False)
                    elif sort_by == 'hl_order':
                        productlist = sorted(productlist, key=lambda x: x.selling_price, reverse=True)
                    elif sort_by == 'ar_order':
                        productlist = sorted(productlist, key=lambda x: x.selling_price, reverse=False)
                    elif sort_by == 'az_order':
                        productlist = sorted(productlist, key=lambda x: x.title.lower(), reverse=False)
                    elif sort_by == 'za_order':
                        productlist = sorted(productlist, key=lambda x: x.title.lower(), reverse=True)
                    else:
                        productlist = sorted(productlist, key=lambda x: x.id, reverse=True)
                    context['sorting'] = sort_by
                else:
                    context['sorting'] = 'lf_order'
                    productlist = sorted(productlist, key=lambda x: x.id, reverse=True)
        except Exception as e:
            print(e, 'clientcategorydetail')
            productlist = Product.objects.filter(is_active=True).order_by('-id')
            category = 'all'
            context['category'] = category
            if sort_by:
                if sort_by == 'lf_order':
                    productlist = productlist.order_by('-id')
                elif sort_by == 'of_order':
                    productlist = productlist.order_by('id')
                elif sort_by == 'lh_order':
                    productlist = productlist.order_by('selling_price')
                elif sort_by == 'hl_order':
                    productlist = productlist.order_by('-selling_price')
                elif sort_by == 'ar_order':
                    productlist = productlist.order_by('selling_price')
                elif sort_by == 'az_order':
                    productlist = productlist.order_by(Lower('title'))
                elif sort_by == 'za_order':
                    productlist = productlist.order_by(Lower('title').desc())
                else:
                    productlist = productlist.order_by('-id')
                context['sorting'] = sort_by
            else:
                context['sorting'] = 'lf_order'
                productlist = productlist.order_by('-id')
        # productlist = Product.objects.filter(category = self.kwargs['pk'])
        page = self.request.GET.get('page', 1)
        paginator = Paginator(productlist, 16)
        try:
            updates = paginator.page(page)
        except PageNotAnInteger:
            updates = paginator.page(1)
        except EmptyPage:
            updates = paginator.page(paginator.num_pages)
        context['productlist'] = updates
        context['categorydetail'] = category
        return context
    

class ClientDashboardView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientdashboard.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            if request.user.is_authenticated and request.user.groups.filter(name="Customer").exists():
                pass
            else:
                messages.error(request, 'Access Denied')
                return redirect('ecomapp:clienthome')
        except Exception as e:
            print(e, 'clientdashboard error')
            messages.error(request, 'Access Denied')
            return redirect('ecomapp:clienthome')
        return super(ClientDashboardView, self).dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["order"] = Order.objects.filter(cart__customer = self.request.user.customer).count()
            # context["wishlist"] = WishList.objects.filter(customer = self.request.user.customer).last()
        return context

class ClientAjaxDashboardView(ClientMixin, View):
    def get(self, request):
        dashboard = self.request.GET.get('dashboard')
        if dashboard == "wishlist":
            wishlist = WishList.objects.filter(customer = self.request.user.customer).last()
            context = {'wishlist':wishlist}
            self.template_name = 'clienttemplates/clientdashboardwishlist.html'
        elif dashboard == 'profile':
            context = {'profile':'profile'}
            self.template_name = "clienttemplates/clientdashboardprofile.html"
        else:
            order= Order.objects.filter(cart__customer = self.request.user.customer)
            page = self.request.GET.get('page', 1)
            paginator = Paginator(order, 12)
            try:
                updates = paginator.page(page)
            except PageNotAnInteger:
                updates = paginator.page(1)
            except EmptyPage:
                updates = paginator.page(paginator.num_pages)
            grand_total = order.aggregate(Sum("nettotal"))["nettotal__sum"]

            context = {'order':updates,"grand_total":grand_total}
            self.template_name = "clienttemplates/clientorderlist.html"
        return render(self.request, self.template_name, context)
    def post(self, request):
        current_password = self.request.POST['oldpword']
        new_password = self.request.POST['newpword']
        conform_password = self.request.POST["conformpword"]
        if new_password != "" and conform_password != "" and current_password !="" and new_password == conform_password:
            user = authenticate(username=request.user.username, password=current_password)
            if user is not None:
                user.set_password(new_password)
                user.save()
                login(self.request, user)
                return JsonResponse({"message":"success"})
            else:
                print("error")
                return JsonResponse({"message":"error"})
        else:
            return JsonResponse({"message":"error"})
            

class ClientAccountSigninView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientaccountsignin.html"


class ClientAboutView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientabout.html"


class ClientContactView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientcontact.html"

    def post(self, request, *args, **kwargs):
        name = self.request.POST['name']
        email = self.request.POST['email']
        phone = self.request.POST['phone']
        message = self.request.POST['message']
        if name == "" and email == "" and phone == "" and message == "":
            return JsonResponse({'message':'error_msg'})
        else:
            Message.objects.create(name = self.request.POST['name'], email= self.request.POST['email'], subject = self.request.POST['subject'], description = self.request.POST['message'], contact_no = self.request.POST['phone'], company = self.request.POST['company'])
            messages.success(request, "Message Sent Ssuccesssffully!!!")

            return JsonResponse({'message':'success'})
    # def get_success_url(self):
    #     return reverse('ecomapp:clienthome')

class ClientWishListView(ClientMixin, ListView):
    template_name = "clienttemplates/wishlist.html"
    model = WishList
    paginate_by = 5

    def dispatch(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(user=request.user)
            pass
        except Exception as e:
            print(e, '\n wishlish unknown user error')
            messages.error(self.request, 'Please login to view your wishlist')
            return redirect('ecomapp:clienthome')
        return super(ClientWishListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wishlistproducts"] = WishList.objects.filter(customer = self.request.user.customer).last() 
        return context
    def post(self, request):
        product_id = self.request.POST["p_id"]
        print(product_id,"++++++++")
        wishList = WishList.objects.filter(customer = self.request.user.customer).last()
        if product_id is not None:
            wishList.products.remove(Product.objects.get(id=product_id))
            count = wishList.products.all().count()
            return JsonResponse({'count':count})
        else:
            count = wishList.products.all().count()
            return JsonResponse({'count':count})

    

class ClientBlogListView(ClientMixin, ListView):
    template_name = "clienttemplates/clientbloglist.html"
    queryset = Blog.objects.all().order_by('-id')
    context_object_name = "bloglist"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featuredbloglist'] = Blog.objects.filter(is_featured=True).order_by('-id')
        return context


class ClientBlogDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientblogdetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogobj = Blog.objects.get(slug = self.kwargs['slug'])
        blogobj.views += 1
        blogobj.save()
        context["trending_blogs"] = Blog.objects.all().order_by('-views')[:10]
        context['featuredbloglist'] = Blog.objects.filter(is_featured=True)
        context['blogdetail'] = blogobj
        context["comments"] = BlogComment.objects.filter(blog=blogobj) 
        return context

    def post(self, request, *args, **kwargs):
        comment = self.request.POST['comment']
        blog = Blog.objects.get(slug = self.kwargs['slug'])
        if comment is not None and comment != "":
            new_comment = BlogComment.objects.create(blog = blog,text=self.request.POST['comment'])
            messages.success(self.request, "comment posted successfully")
            message='success'
        else:
            message = "Emty Comment"
        return JsonResponse({
            'message':message
        })


class ClientSignupView(ClientMixin, CreateView):
    template_name = "clienttemplates/clientsignup.html"
    form_class = CustomerForm
    success_url = "/"
    success_message = "Signup Successfully!!!"

    def form_valid(self, form):
        # username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        if User.objects.filter(username=email).exists():
            return render(self.request, self.template_name, {'form': form, 'errors': 'User Already Exist!'})
        else:
            user = User.objects.create_user(email, email, password)
        form.instance.user = user

        return super().form_valid(form)


class ClinetCollectionDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clinetcollectiondetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collectiondetail"] = Collection.objects.get(id = self.kwargs["pk"]) 
        return context

class ClientSupportView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientsupport.html"

class ClientPrivacyView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientprivacy.html"

class ClientTemrsofuseView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clienttermsofuse.html"
    

# Client Ajax View
# ajax customer registration
class AjaxClientCustomerRegistrationView(View):
    def post(self, request, *args, **kwargs):
        fullname = request.POST.get("fullName")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(email, email, password)
            customer = Customer.objects.create(user=user, name=fullname)
            WishList.objects.create(customer = customer)
            usr = authenticate(username=email, password=password)
            if usr is not None:
                login(self.request, user)
            return JsonResponse({'message': 'success'})
        except Exception as e:
            print(e, 'ajaxclientcustomerregistrationview')
            return JsonResponse({"message": "error"})

class AjaxClientCustomerLogInView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        # print(email)
        password = request.POST.get("password")
        # print(password)
        user = authenticate(username=email, password=password)
        try:
            if user is not None:
                try:
                    customer = user.customer
                    login(self.request, user)
                    messages.success(self.request, f'Logged in as {user.username}')
                    return JsonResponse({'message':'success'})
                except Exception as e:
                    print(e, 'clientlogin error')
                    messages.error(self.request, 'Invalid Email or Password')
                    return JsonResponse({'message':'Invalid Email or Password'})
            else:
                print('login eror client')
                messages.error(self.request, 'some errors')
                return JsonResponse({'message':'Invalid Email or Password'})
        except Exception as e:
            print(e, '\njjjjjjjjjjjj')
            messages.error(self.request, 'some errors')
            return JsonResponse({'message': 'error'})


class AjaxClientAddToCartView(View):
    def get(self, request, *args, **kwargs):
        print(request.GET.get('quantity'))
        try:
            item_quantity = int(request.GET.get('quantity'))
            # total_quantity += item_quantity
        except Exception as e:
            print(e, '\n 0 quantity, quantity error')
            item_quantity = 0
        if item_quantity < 1 or item_quantity > 10:
            print('quantity failure')
            return JsonResponse({"message": 'failure'})
        else:
            try:
                product = Product.objects.get(id=self.kwargs['pk'])
                cart_id = request.session.get('mycart', None)
                try:
                    cart = Cart.objects.get(id=cart_id)
                except Exception as e:
                    print(e)
                    cart = Cart.objects.create(subtotal=0, discount=0, nettotal=0)
                    request.session['mycart'] = cart.id

                cartproducts = CartProduct.objects.filter(cart = cart)
                total_quantity = cartproducts.aggregate(Sum("quantity"))["quantity__sum"]
                if total_quantity is None:
                    total_quantity = 1
                cartproduct_query = cart.cartproduct_set.filter(product=product)

                if cartproduct_query.exists():
                    cartproduct = cartproduct_query.first()
                    cartproduct.quantity += item_quantity
                    cartproduct.subtotal = cartproduct.quantity * cartproduct.rate
                    cartproduct.save()
                else:
                    cartproduct = CartProduct.objects.create(
                        cart=cart, product=product,
                        rate=product.selling_price,
                        quantity=item_quantity,
                        subtotal=product.selling_price * item_quantity)
                cart.subtotal += cartproduct.rate * item_quantity
                cart.nettotal += cartproduct.rate * item_quantity
                cart.save()
                try:
                    order = cart.order
                    if order:
                        shipping_charge = 0
                        for cp in cart.cartproduct_set.all():
                            shipping_charge += cp.shipping_charge
                        order.shipping_charge = shipping_charge
                        order.subtotal = cart.subtotal
                        order.discount = cart.discount
                        order.total = cart.nettotal
                        order.nettotal = order.total + order.shipping_charge
                        order.save()
                except Exception as e:
                    print(e, '\n no order of cart')
                return JsonResponse({"message": "success", 'addedproduct': product.title,})
            except Exception as e:
                print(e, '\naddtocart error')
                return JsonResponse({"message": 'failure'})


class AjaxClientUpdateCartProductsQuantityView(View):
    def post(self, request, *args, **kwargs):
        lists = request.POST.getlist('series[]')
        cart_id = request.POST.get('c_id')
        message = 'success'
        # print(lists)
        try:
            for i in lists:
                split_data = i.split('_%_')
                cartproduct = CartProduct.objects.get(id=split_data[1])
                quantity = split_data[0]
                cartproduct.quantity = quantity
                cartproduct.subtotal = cartproduct.rate * int(quantity)
                cartproduct.save()
            cart = Cart.objects.get(id=cart_id)
            subtotal = 0
            for product in cart.cartproduct_set.all():
                subtotal += product.subtotal

            cart.subtotal = subtotal
            cart.nettotal = subtotal
            cart.save()
        except Exception as e:
            print(e)
            message = 'error'
        try:
            order = cart.order
            if order:
                shipping_charge = 0
                for cp in cart.cartproduct_set.all():
                    shipping_charge += cp.shipping_charge
                order.shipping_charge = shipping_charge
                order.subtotal = cart.subtotal
                order.discount = cart.discount
                order.total = cart.nettotal
                order.nettotal = order.total + order.shipping_charge
                order.save()
                # messages.success(self.request, "Cart updated successfully")
        except Exception as e:
            print(e)
            message = 'error_noorder'
            # messages.error(request, "Failed process")
        if message == 'success':
            messages.success(self.request, "Cart updated successfully")
        return JsonResponse({"message": message})


class AjaxClientManageCartView(View):
    def get(self, request, *args, **kwargs):
        cp_id = request.GET.get('id')
        action = request.GET.get('action')
        try:
            cart_product = CartProduct.objects.get(id=cp_id)
            subtotal = cart_product.subtotal
            cart = cart_product.cart
            if action == 'rmv':
                cart_product.delete()
            else:
                print('some error')
            # cart.subtotal = cart.subtotal - subtotal
            # cart.nettotal = cart.nettotal - subtotal
            # cart.save()
            subtotal = 0
            for product in cart.cartproduct_set.all():
                subtotal += product.subtotal

            cart.subtotal = subtotal
            cart.nettotal = subtotal
            cart.save()

            try:
                order = cart.order
                if order:
                    shipping_charge = 0
                    for cp in cart.cartproduct_set.all():
                        shipping_charge += cp.shipping_charge
                    order.shipping_charge = shipping_charge
                    order.subtotal = cart.subtotal
                    order.discount = cart.discount
                    order.total = cart.nettotal
                    order.nettotal = order.total + order.shipping_charge
                    order.save()
            except Exception as e:
                print(e)

            return JsonResponse({"message": 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'fail'})


class AjaxClientCityListView(View):
    def get(self, request, *args, **kwargs):
        region = Region.objects.filter(slug=request.GET['slug']).last()
        if region:
            city = City.objects.filter(region=region).order_by('title')
            return render(request, 'clienttemplates/clientcitylist.html', {'cities': city, 'message': 'success'})
        else:
            return JsonResponse({'message': 'error'})

class AjaxSuscriberCreate(View):
    def post(self, request):
        email = self.request.POST['suscriber']
        if email is not None and email != "":
            if Subscriber.objects.filter(email = email).exists():
                messages.error(request, "Failed Successfully!!!")
                return JsonResponse({'result':'error'})
            else:
                Subscriber.objects.create(email = email)
                messages.success(request, "Created Successfully!!!")
                return JsonResponse({'result':'success'})
        else:
            return JsonResponse({'result':'failure'})


class AjaxSearchProductsView(View):
    def get(self, request):
        try:
            keyword = request.GET.get("keyword")
            if len(keyword) >= 3:
                productlist = Product.objects.filter(Q(title__icontains = keyword)|Q(product_code__icontains = keyword)|Q(category__title__icontains = keyword)|Q(meta_description__icontains = keyword)|Q(description__icontains = keyword))

            context = {
                "productlist":productlist,
                "keyword":keyword,
            }
            return render(request, "clienttemplates/searchresults.html", context)
        except Exception as e:
            print(e, 'ajaxsearchproductview')
            return JsonResponse({"message": 'error'})


class ClientSearchView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientsearch.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            keyword = self.request.GET.get("keyword")
            cat_slug = self.request.GET.get('cat')
            sort_by = self.request.GET.get('sorting')
            if len(keyword) >= 3:
                if cat_slug != 'all':
                    try:
                        category = Category.objects.get(slug=cat_slug, is_active=True)
                        if category.root: 
                            productlist = Product.objects.filter(Q(title__icontains = keyword)|Q(product_code__icontains = keyword)|Q(meta_description__icontains = keyword)|Q(description__icontains = keyword), category=category, is_active=True)
                        else:
                            categories = Category.objects.filter(root=category, is_active=True)
                            productlist = Product.objects.filter(Q(title__icontains = keyword)|Q(product_code__icontains = keyword)|Q(meta_description__icontains = keyword)|Q(description__icontains = keyword), category__in=categories, is_active=True)
                    except Exception as e:
                        print(e, 'clientsearchview error')
                        productlist = Product.objects.filter(Q(title__icontains = keyword)|Q(product_code__icontains = keyword)|Q(category__title__icontains = keyword)|Q(meta_description__icontains = keyword)|Q(description__icontains = keyword), is_active=True)
                else:
                    productlist = Product.objects.filter(Q(title__icontains = keyword)|Q(product_code__icontains = keyword)|Q(category__title__icontains = keyword)|Q(meta_description__icontains = keyword)|Q(description__icontains = keyword), is_active=True)
                if sort_by:
                    if sort_by == 'lf_order':
                        productlist = productlist.order_by('-id')
                    elif sort_by == 'of_order':
                        productlist = productlist.order_by('id')
                    elif sort_by == 'lh_order':
                        productlist = productlist.order_by('selling_price')
                    elif sort_by == 'hl_order':
                        productlist = productlist.order_by('-selling_price')
                    elif sort_by == 'ar_order':
                        productlist = productlist.order_by('selling_price')
                    elif sort_by == 'az_order':
                        productlist = productlist.order_by(Lower('title'))
                    elif sort_by == 'za_order':
                        productlist = productlist.order_by(Lower('title').desc())
                    else:
                        productlist = productlist.order_by('-id')
                    context['sorting'] = sort_by
                else:
                    context['sorting'] = 'lf_order'
                    productlist = productlist.order_by('-id')
                context['count'] = productlist.count()
                page = self.request.GET.get('page', 1)
                paginator = Paginator(productlist, 12)
                try:
                    updates = paginator.page(page)
                except PageNotAnInteger:
                    updates = paginator.page(1)
                except EmptyPage:
                    updates = paginator.page(paginator.num_pages)
                print(cat_slug)
                context['searchresults'] = updates
                context["keyword"] = keyword
                context['cat_slug'] = cat_slug
        except Exception as e:
            print(e, 'ajaxsearchproductview')
            context['productlist'] = 'none'

        return context


class ClientProductQuickView(ClientMixin, View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        return render(request, 'clienttemplates/clientproductquickview.html', {'product':product})


class ClientShopView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientshop.html"

    


# class ClientajaxgetsubcategotiesView(ClientMixin,View):
#     def get(self,request):
#         cat_obj = Category.objects.filter(id = self.request.GET.get("main_cat_id")).last()
#         sub_cat = Category.objects.filter(root = cat_obj)
#         return render(request, "clienttemplates/sub_cat.html", {"sub_cat":sub_cat})
        # return JsonResponse({"sub_cat":sub_cat})

class ClientShopCategoryDetailView(ClientMixin, TemplateView):
    template_name = "clienttemplates/clientshopcategorydetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

#forgot password

class ClientForgetPasswordView(ClientMixin,View):
    def get(self, request):
        email = request.GET.get("email")
        user = User.objects.filter(username = email).last()   
        if Customer.objects.filter(user=user).exists():
            print(user.customer)
            domain = self.request.META['HTTP_HOST']
            text_content = 'Please Click The Link Below!!'
            html_content = domain + "/client" + "/password-reset/" + email + \
                "/" + password_reset_token.make_token(user) + "/"
            send_mail(
                'Password Reset Link',
                text_content + html_content,
                settings.EMAIL_HOST_USER,
                (email,),
                fail_silently=False,
            )
            return JsonResponse({"message":"success"})
        else:
            return JsonResponse({'message':"error"})

class ClientPassordResetView(ClientMixin, FormView):
    template_name = 'clienttemplates/forgotpaswordreset.html'
    form_class = ClientPasswordResetForm
    success_url = reverse_lazy('ecomapp:clientlogin') 

    def form_valid(self, form):
        password = form.cleaned_data['confirm_password']
        print(password)
        email = self.kwargs['email']
        user = User.objects.get(username = email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        print("error")
        return super().form_invalid(form)

class ClientProfileUpdateView(ClientMixin, UpdateView):
    template_name = "clienttemplates/clientprofileupdate.html"
    model = Customer
    form_class = ClientProfileForm
    success_url = reverse_lazy("ecomapp:clientdashboard")
    success_message = "Profile Updated Successfully"

class ClientQuotationView(ClientMixin, CreateView):
    template_name = "clienttemplates/clientquotation.html"
    form_class = QuotationForm
    success_url = reverse_lazy("ecomapp:clienthome")
    success_message = "Quotation requested successfully!!"

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.name = self.request.user.customer.name
            form.save()
        return super().form_valid(form)

