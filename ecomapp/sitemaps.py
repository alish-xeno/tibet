from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, Blog, Product


class StaticViewSiteMap(Sitemap):
    protocol = "https"

    def items(self):
        return ['clienthome', 'clientbloglist', 'clientcontact', 'clientabout', 'clientallproducts', 'clientsignup', 'clientlogin', 'clientsupport', 'clientprivacy', 'clienttermsofuse', 'clientsearch', 'clientshop']

    def location(self, items):
        return reverse("ecomapp:" + items)


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Category.objects.filter().order_by("-id")


class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Product.objects.all().order_by("-id")


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Blog.objects.filter().order_by("-id")