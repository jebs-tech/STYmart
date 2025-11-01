from django.urls import path
from main.views import (
    show_main, create_product, show_product, edit_product, delete_product,
    register, login_user, logout_user,
    show_json, show_json_by_id, show_xml_by_id, show_xml,
    add_products_entry_ajax, update_product_ajax, delete_product_ajax,
    login_ajax, register_ajax, logout_ajax, add_to_cart
)

app_name = 'main'

urlpatterns = [
    # Pages (normal)
    path('', show_main, name='show_main'),
    path('create-product/', create_product, name='create_product'),
    path('product/<int:id>/', show_product, name='show_product'),
    path('product/<int:id>/edit/', edit_product, name='edit_product'),
    path('product/<int:id>/delete/', delete_product, name='delete_product'),

    # Data (JSON/XML)
    path('json/', show_json, name='show_json'),
    path('json/<int:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/<int:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('xml/', show_xml, name='show_xml'),

    # Auth pages
    path("register/", register, name="register"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),

    # AJAX CRUD
    path('ajax/product/create/', add_products_entry_ajax, name='add_products_entry_ajax'),
    path('ajax/product/<int:id>/update/', update_product_ajax, name='update_product_ajax'),
    path('ajax/product/<int:id>/delete/', delete_product_ajax, name='delete_product_ajax'),

    # AJAX Auth
    path('ajax/login/', login_ajax, name='login_ajax'),
    path('ajax/register/', register_ajax, name='register_ajax'),
    path('ajax/logout/', logout_ajax, name='logout_ajax'),

    # Helper Cart for fixing Detail Product Error
    path('product/<int:id>/add-to-cart/', add_to_cart, name='add_to_cart'),
]
