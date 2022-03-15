from django import forms
from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import requests



class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter email",
        # 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Password"
    }))
class OrganizationForm(forms.ModelForm):
    class Meta:
        model = OrganizationInformation
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
                }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class':'form-control',
                'accept': 'image/*',
                }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
                }),
            'slogan': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Slogan"
                }),
            'contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{6,15}',
                'placeholder': "Enter Contact No.",
                }),
            'alt_contact_no':forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{6,15}',
                'placeholder': "Enter Alternate Contact No.",
                }),
            'map_location':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Map Location",
                }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': "Enter Email",
                }),
            'alt_email': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter Alternate Email',
                }),
            'about_us': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Tell us about your Organization',
					'height': '300px',
                    }
				}),
            'facebook':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Facebook Id",
                }),
            'instagram':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Instagram Id",
                }),
            'youtube':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Youtube Link",
                }),
            'twitter':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Twitter Id",
                }),
            'viber':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Viber Number",
                }),
            'seller_policy': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Tell us about your Seller Policy',
					'height': '300px'
                    }
				}),
            'return_policy': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Tell us about your Return Policy',
					'height': '300px'
                    }
				}),
            'support_policy': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Support policy',
					'height': '300px'
                    }
				}),
            'terms_conditions': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Terms and condition',
					'height': '300px'
                    }
				}),
            'privacy_policy': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Tell us about your Privacy Policy',
					'height': '300px'
                    }
				}),
    #         'terms_condition': SummernoteWidget(attrs={
				# 'summernote': {
				# 	'class': 'form-control',
				# 	'placeholder': 'Tell us about your Terms and Conditions',
				# 	'height': '300px'
    #                 }
				# }),
            'return_policy_for_products': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Tell us about your Return Policy for Products',
					'height': '300px'
                    }
				}),
            'meta_description':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Meta Description",
                }),
            'fb_messenger_script':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Facebook Messenger Script",
                }),
            'google_analytics_script':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Google Analytics Script",
                }),
            'fb_pixel_script':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Enter Facebook Pixel Script",
                }),
            'detail_pixel': SummernoteWidget(attrs={
				'summernote': {
					'class': 'form-control',
					'placeholder': 'Enter Detail Pixel',
					'height': '300px'
                    }
				}),
            }


class AdminCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'image', 'mobile', 'street_address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile',
                'pattern': '[0-9]{6,15}',
                }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address'
                }),
        }


class AdminCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'slug', 'image', 'banner', 'root', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug',
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'banner': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'root': forms.Select(attrs={
                'class': 'form-control'
                }),
            'is_featured': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
                }),
        }
    def __init__(self, *args, **kwargs):
        super(AdminCategoryForm, self).__init__(*args, **kwargs)
        self.fields['root'].queryset = Category.objects.filter(root=None)


class AdminProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'product_code', 'category', 'display_image', 'meta_description', 
                'description', 'return_policy', 'warranty', 'on_sale', 'marked_price', 
                'selling_price','is_featured']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title',
                }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Slug',
                }),
            'product_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Code',
                }),
            'category': forms.Select(attrs={
                'class': 'form-control'
                }),
            'display_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'meta_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Meta Description',
                }),
            'description': SummernoteWidget(attrs={
                'summernote': {
                    'class': 'form-control',
                    'placeholder': 'Product Description',
                    'height': '300px'
                    }
                }),
            'return_policy': SummernoteWidget(attrs={
                'summernote': {
                    'class': 'form-control',
                    'placeholder': 'Tell us about your Return Policy',
                    'height': '300px'
                    }
                }),
            'warranty': SummernoteWidget(attrs={
                'summernote': {
                    'class': 'form-control',
                    'placeholder': 'Tell us about your Warranty',
                    'height': '300px'
                    }
                }),
            'is_featured': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
                }),
            'on_sale': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
                }),
            'marked_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Marked Price'
                }),
            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Selling Price'
                }),
        }

    def __init__(self, *args, **kwargs):
        super(AdminProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(root__isnull=False)

class SliderCreateForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ["title", 'image', 'action_link_name', "action_link", 'caption']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':'Title'
            }),
            'image':forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'action_link_name':forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':'Action Link Name'
            }),
            'action_link':forms.TextInput(attrs={
                'class':"form-control",
                'placeholder':'Action Link'
            }),

            'caption':forms.Textarea(attrs={
                'class':"form-control",
                'placeholder':'Caption',
                'rows': '7'
            }),
        }

class AdminBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','image','content','is_featured']
        widgets = {
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Title'
            }),
            'image':forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'content':SummernoteWidget(attrs={
                'class':"form-control",
                'placeholder':'Caption',
                'height':"300px"
            }),
            'author':forms.Select(attrs={
                'class':'form-control'
            }),
            'is_featured':forms.CheckboxInput()
        }

    # def __init__(self, *args, **kwargs):
    #     super(AdminBlogForm, self).__init__(*args, **kwargs)
    #     self.fields['author'].queryset = EcommerceAdmin.objects.all()

class AdminRegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['title', 'slug']
        widgets = {
            'title':forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':'Title'
                }),
            'slug':forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':'Slug',
                    'readonly':'readonly',

                }),
        }

class AdminCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['title', 'slug', 'region', 'default_shipping_charge']
        widgets = {
            'title':forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':'Title'
                }),
            'slug':forms.TextInput(attrs={
                    'class':'form-control',
                    'placeholder':'Slug',
                    'readonly':'readonly',

                }),
            'region':forms.Select(attrs={
                    'class':'form-control',
                    'placeholder':'Region'
                }),
            'default_shipping_charge':forms.NumberInput(attrs={
                'class':'form-control',
                'placehlder':'25'
            })            
}

class AdminFaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ("question","answer")
        widgets = {
            'question':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Question'
            }),
            'answer':forms.Textarea(attrs = {
                'class':'form-control',
                'placeholder':'Answer'
            })
        }
class AdminSuscriberForm(forms.ModelForm):
    
    class Meta:
        model = Subscriber
        fields = ["email"]
        
        widgets = {
            'email':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Email'
            })
        }


        

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['subtotal', 'discount', 'total', 'shipping_charge', 'shipping_charge_discount', 
                'nettotal', 'customer_payment_status', 'requested_shipping_date', 
                'name', 'mobile', 'email', 'region', 'city', 'street_address', 'is_complete', 
                'completed_date', 'order_status', 'note']
        widgets = {
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subtotal'
                }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Discount'
                }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Total'
                }),
            'shipping_charge': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shipping Charge'
                }),
            'shipping_charge_discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Shipping Charge Discount'
                }),
            'nettotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nettotal'
                }),
            'customer_payment_status': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
                }),
            'requested_shipping_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
                }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name',
                }),
            'mobile': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile',
                'pattern': '[0-9]{6,15}',
                }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': "Enter Email",
                }),
            'region': forms.Select(attrs={
                'class': 'form-control'
                }),
            'city': forms.Select(attrs={
                'class': 'form-control'
                }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Street Address",
                }),
            'is_complete': forms.CheckboxInput(attrs={
                # 'class': 'form-control'
                }),
            'completed_date': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD'
                }),
            'order_status': forms.Select(attrs={
                'class': 'form-control'
                }),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Note',
                }),
        }

class CustomerLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': "Enter email",
        'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': "Password"
    }))    

class CustomerForm(forms.ModelForm):
    recaptcha = forms.CharField(widget=forms.TextInput(attrs={
        "hidden":True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control signup-email',
        'id': 'su-email',
        'placeholder': "Enter email",
        'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'su-password',
        'placeholder': "Password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'su-password-confirm',
        'placeholder': "Confirm Password"
    }))
    class Meta:
        model = Customer
        fields = ['name', 'email', 'password', 'confirm_password']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control signup-fullname',
                'id': 'su-name',
                'placeholder': 'Full Name',
                }),
            # 'image': forms.ClearableFileInput(attrs={
            #     'class': 'form-control',
            #     }),
            # 'mobile': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Mobile',
            #     'pattern': '[0-9]{6,15}',
            #     }),
            # 'street_address': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Street Address'
            #     }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('email')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        recaptcha = self.cleaned_data.get("recaptcha")
        data = {
        "secret": "6Lfs4nYbAAAAAMvHazmJaWJbjjysxtczJ0NiFNcv",
        "response": recaptcha
        }
        resp = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data).json()
        if resp["success"] is True:
            pass
        else:
            raise forms.ValidationError("Captcha Error")


class ClientOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['requested_shipping_date', 'name', 'last_name', 'mobile', 'email', 'street_address']
        widgets = {
            'requested_shipping_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                }),
            'mobile': forms.NumberInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{6,15}',
                }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                # 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'pattern': '^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                }),
        }    

class ClientPasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control password-box',
        'placeholder':'New Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control password-box',
        'placeholder':'Confirm Password'
    }))

    def clean_confirm_password(self):
        npword = self.cleaned_data['new_password']
        cpword = self.cleaned_data['confirm_password']

        if npword != cpword:
            raise forms.ValidationError('Password did not match!!!')
        
        return cpword  

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'image', 'mobile', 'street_address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile',
                'pattern': '[0-9]{6,15}',
                }),
            'street_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Street Address'
                }),
        }  

class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ['name','mobile','address','email','company','products','details']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name',
                }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile',
                'pattern': '[0-9]{6,15}',
                }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Address'
                }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder":"Email",
                'pattern': '^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
                }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Company Name'
                }),
            'products': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder':'Choose product'
                }),
            'details': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder':'Details'
                }),
        }

#end