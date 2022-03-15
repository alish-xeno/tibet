from django.urls import path
from .views import *
from .sitemaps import *
from django.contrib.sitemaps.views import sitemap

app_name = "ecomapp"

sitemaps = {
	'static': StaticViewSiteMap,
	'category': CategorySitemap,
	'products': ProductSitemap,
	'blogs': BlogSitemap,
}

urlpatterns = [
	path("sitemap/sitemap.xml", sitemap, {"sitemaps": sitemaps}),
	path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
	
	
	# Admin Urls
	#amdin login
	path("ecomm-admin/login/", AdminLoginView.as_view(), name = 'adminlogin'),
	path("ecomm-admin/logout/", AdminLogoutView.as_view(), name = 'adminlogout'),
	path('ecomm-admin/', AdminHomeView.as_view(), name="admindashboard"),
	path("ecomm-admin/home/", AdminHomeView.as_view(), name="adminhome"),
	path("ecomm-admin/detail/", AdminOrganizationDetailView.as_view(), 
		name="adminorganizationdetail"),
	path("ecomm-admin/org/<int:pk>/update/", AdminOrganizationUpdateView.as_view(), 
		name="adminorganizationupdate"),

	path("ecomm-admin/customer/list/", AdminCustomerListView.as_view(), 
		name="admincustomerlist"),
	path("ecomm-admin/customer/<int:pk>/detail/", AdminCustomerDetailView.as_view(), 
		name="admincustomerdetail"),
	path("ecomm-admin/customer/<int:pk>/update/", AdminCustomerUpdateView.as_view(), 
		name="admincustomerupdate"),
	#ecommerce admins
	path('ecomm-admin/admin/list/',AdminEcomAdminList.as_view(), name = "adminecomadminlist"),

	# Admin Category URL
	path("ecomm-admin/product-category/list/", AdminCategoryListView.as_view(), 
		name="admincategorylist"),
	path("ecomm-admin/product-category/create/", AdminCategoryCreateView.as_view(), 
		name="admincategorycreate"),
	path("ecomm-admin/product-category/<int:pk>/update/", AdminCategoryUpdateView.as_view(), 
		name="admincategoryupdate"),

	# Admin Product Url
	path("ecomm-admin/product/list/", AdminProductListView.as_view(), 
		name="adminproductlist"),
	path("ecomm-admin/product/create/", AdminProductCreateView.as_view(), 
		name="adminproductcreate"),
	path("ecomm-admin/product/<int:pk>/update/", AdminProductUpdateView.as_view(), 
		name="adminproductupdate"),
	path("ecomm-admin/product/<int:pk>/detail/", AdminProductDetailView.as_view(), 
		name="adminproductdetail"),

	# Admin Product image manage
	path("ecomm-admin/product/<int:pk>/image-management/", AdminProductImageManageView.as_view(), 
		name="adminproductimagemanage"),

	#admin slider
	path("ecomm-admin/slider/list/", AdminSliderListView.as_view(), name='adminsliderlist'),
	path("ecomm-admin/slider/<int:pk>/detail/", AdminSliderDetailView.as_view(), name='adminsliderdetail'),
	path("ecomm-admin/slider/create/", AdminSliderCreateView.as_view(), name='adminslidercreate'),
	path("ecomm-admin/slider/<int:pk>/update/", AdminSliderUpdateView.as_view(), name='adminsliderupdate'),

	# admin-blog
	path("ecomm-admin/blog/list/", AdminBlogListView.as_view(), name = "adminbloglist"),
	path("ecomm-admin/blog/create/", AdminBlogCreateView.as_view(), name = "adminblogcreate"),
	path("ecomm-admin/blog/<int:pk>/update/", AdminBlogUpdateView.as_view(), name = "adminblogupdate"),
	path("ecomm-admin/blog/<int:pk>/detail/", AdminBlogDetailView.as_view(), name = "adminblogdetail"),

	#admin-region
	path("ecomm-admin/region/list/", AdminRegionListView.as_view(), name = "adminregionlist"),
	path("ecomm-admin/region/<int:pk>/detail/", AdminRegionUpdateView.as_view(), name = "adminregionupdate"),
	path("ecomm-admin/region/create/", AdminRegionCreateView.as_view(), name = "adminregioncreate"),

	#admin-city
	path("ecomm-admin/city/list/", AdminCityListView.as_view(), name = "admincitylist"),
	path("ecomm-admin/city/<int:pk>/detail/", AdminCityUpdateView.as_view(), name = "admincityupdate"),
	path("ecomm-admin/city/create/", AdminCityCreateView.as_view(), name = "admincitycreate"),

	#admin faq
	path("ecomm-admin/faq/list/", AdminFAQListView.as_view(), name = "adminfaqlist"),
	path("ecomm-admin/faq/<int:pk>/detail/", AdminFAQDetailView.as_view(), name = "adminfaqdetail"),
	path("ecomm-admin/faq/create/", AdminFAQCreateView.as_view(), name = "adminfaqcreate"),
	path("ecomm-admin/faq/<int:pk>/update/", AdminFAQUpdateView.as_view(), name = "adminfaqupdate"),

	#admin suscribers
	path("ecomm-admin/suscriber/list/", AdminSuscriberListView.as_view(), name = 'adminsuscriberlist'),

	#admin quotation
	path("ecomm-admin/quotation/list/", AdminQuotationListView.as_view(), name = "adminquotationlist"),
	path("ecomm-admin/quotation/<int:pk>/detail/", AdminQuotationDetailView.as_view(), name = "adminquotationdetail"),

	#admin message
	path('ecomm-admin/message/list/', AdminMessageListView.as_view(), name = "adminmessagelist"),
	path('ecomm-admin/message/<int:pk>/detail/', AdminMessageDetailView.as_view(), name = "adminmessagedetail"),

	# Admin Order Url
	path("ecomm-admin/order/list/", AdminOrderListView.as_view(), 
		name="adminorderlist"),
	path("ecomm-admin/order/<int:pk>/update/", AdminOrderUpdateView.as_view(), 
		name="adminorderupdate"),
	path("ecomm-admin/order/<int:pk>/detail/", AdminOrderDetailView.as_view(), 
		name="adminorderdetail"),


	# CLient urls
    path("", ClientHomeView.as_view(), name="clienthome"),
	path("shop/<product_title>/<slug:slug>/", ClientProductDetailView.as_view(), name="clientproductdetail"),
	path("cart/", ClientCartDetailView.as_view(), name="clientcartdetail"),
	path("checkout/", ClientCheckoutView.as_view(), name="clientcheckout"),
	path('checkout/order-a1s2n33<int:pk>/asn278/', ClientOrderUpdateView.as_view(), name="clientorderupdate"),
	path("checkout/payment/", ClientCheckoutPaymentView.as_view(), name="clientcheckoutpayment"),
	path("checkout-review/", ClientCheckoutReviewView.as_view(), name="clientcheckoutreview"),
	path("checkout-complete/", ClientCheckoutCompleteView.as_view(), name="clientcheckoutcomplete"),
	path("dashboard/", ClientDashboardView.as_view(), name="clientdashboard"),
	path('order/<int:pk>/detail/', ClientOrederDetailView.as_view(), name = "clientorderdetail"),
	path("account/signin/", ClientAccountSigninView.as_view(), name="clientaccountsignin"),
	path("about/", ClientAboutView.as_view(), name="clientabout"),
	path("contact/", ClientContactView.as_view(), name='clientcontact'),
	path("blogs/", ClientBlogListView.as_view(), name="clientbloglist"),
	path("blog/<slug:slug>/", ClientBlogDetailView.as_view(), name="clientblogdetail"),
	path('category/<slug:slug>/all-products/', ClientCategoryDetailView.as_view(), name="clientcategorydetail"),
	path('allproducts/', ClientAllProducts.as_view(), name = 'clientallproducts'),
	path("signup/", ClientSignupView.as_view(), name="clientsignup"),
	path("signin/", ClientLoginView.as_view(), name = 'clientlogin'),
	# path('change-passord/', ClientChangePasswordView.as_vieww(), name = 'clientchangepassword'),
	path('signout/', ClientLogoutView.as_view(), name = 'clientsignout'),
	path('wishlist/', ClientWishListView.as_view(), name = "wishlist"),
	path("collection/detail/<int:pk>/", ClinetCollectionDetailView.as_view(), name = "collectiondetail"),
	path("support", ClientSupportView.as_view(), name = "clientsupport"),
	path("privacy-policy/", ClientPrivacyView.as_view(), name = "clientprivacy"),
	path("terms-of-use/", ClientTemrsofuseView.as_view(), name = "clienttermsofuse"),
	path("ajax/search/products/", AjaxSearchProductsView.as_view(), name = "ajaxsearchproducts"),
	path("client/profile/update/<int:pk>/", ClientProfileUpdateView.as_view(), name = "clientprofileupdate"),
	path("client/quotation/", ClientQuotationView.as_view(), name = "clientquotation"),
	path("search/", ClientSearchView.as_view(), name="clientsearch"),

	path('quick-view/product/<int:pk>/', ClientProductQuickView.as_view(), name="clientproductquickview"),

	path('shop/', ClientShopView.as_view(), name="clientshop"),


	#forgot password
	path('client/forgot-password/', ClientForgetPasswordView.as_view(), name = "clientforgetpassword"),
    path('client/password-reset/<email>/<token>/', ClientPassordResetView.as_view(), name = 'clientpasswordreset'),
	

	# Ajax view clients
	# ajax customer create
	path("ajax/customer/registration/", AjaxClientCustomerRegistrationView.as_view(), 
		name="ajaxcustomerregistration"),
	path("ajax/customer/login/", AjaxClientCustomerLogInView.as_view(), name = "ajaxcustomerlogin"),

	path("ajax/customer/add-to-cart/<int:pk>/", AjaxClientAddToCartView.as_view(), 
		name="ajaxcustomeraddtocart"),
	path("ajax/customer/update/cart-products/quantity/", AjaxClientUpdateCartProductsQuantityView.as_view(), 
		name="ajaxcustomerudpatecartproductquantity"),
	path("ajax/customer/manage-cart/", AjaxClientManageCartView.as_view(), 
		name="ajaxcustomermanagecart"),

	path('ajax/customer/add-to-wishlist/', ClientAddToWishlist.as_view(), 
		name="ajaxcustomeraddtowishlist"),

	path("ajax/customer/city-from-region/list/", AjaxClientCityListView.as_view(), 
		name="ajaxcustomercitylist"),
	path("ajax/create/suscriber/", AjaxSuscriberCreate.as_view(), name = "createsuscrber"),

    path("shop/category/", ClientShopCategoryDetailView.as_view(), name="clientshopcategorydetail"),
	path("dashboard/ajax/", ClientAjaxDashboardView.as_view(), name = 'clientajaxdashboard'),
	# path("ajax/get/sub-categories/", ClientajaxgetsubcategotiesView.as_view(), name = "ajaxgetsubcategories")
]