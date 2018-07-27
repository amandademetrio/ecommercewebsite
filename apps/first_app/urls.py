from django.conf.urls import url
from . import views

urlpatterns = [
    #Rendering routes
    url(r'^$', views.index),
    url(r'admin$', views.loadadmin),
    url(r'product/(?P<number>[0-9]+)$', views.loadproduct),
    url(r'loadcart$', views.loadcart),
    url(r'ordersuccess$', views.ordersuccess),
    url(r'category/(?P<number>[0-9]+)$', views.cat_page),
    url(r'dashboard/orders$', views.adminorders),
    url(r'dashboard/products$', views.adminproducts),
    url(r'dashboard/orders/(?P<number>[0-9]+)$', views.adminoneorder),

    #Admin process routes
    url(r'dashboard/products/find$',views.find_product),
    url(r'dashboard/products/add$',views.add_product),
    url(r'dashboard/products/update$',views.edit_product),
    url(r'dashboard/products/delete$',views.delete_product),
    url(r'dashboard/orders/find$',views.find_order),
    url(r'dashboard/orders/sort$',views.sort_order),
    url(r'dashboard/orders/change_status$',views.change_status),

    #Admin login and registration
    url(r'admin/processregistration$', views.registration),
    url(r'admin/logout$', views.logout),
    url(r'admin/login$', views.login),

    #Regular user processing routes
    url(r'add_to_cart$', views.add_to_cart),
    url(r'product/find$', views.user_product_find),
    url(r'orders/submit$', views.submit_order),
    url(r'product/find/category$', views.user_product_find_cat),
    url(r'remove_from_cart$', views.remove_from_cart),

] 