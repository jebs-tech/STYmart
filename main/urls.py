from django.urls import path
from main.views import (
    show_main,
    register,
    login_user,
    logout_user,
    create_product_ajax,
    edit_product_ajax,
    delete_product_ajax,
    show_json_by_id,
    show_xml,
    show_xml_by_id,
)
app_name = 'main'

urlpatterns = [
    # MAIN
    path('', show_main, name='show_main'),

    # PRODUCT CRUD (non-AJAX)


    # PRODUCT CRUD (AJAX)
    path('ajax/product/create/', create_product_ajax, name='create_product_ajax'),
    path('ajax/product/<int:product_id>/edit/', edit_product_ajax, name='edit_product_ajax'),
    path('ajax/product/<int:product_id>/delete/', delete_product_ajax, name='delete_product_ajax'),

    # API JSON / XML
    path('json/<int:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<int:product_id>/', show_xml_by_id, name='show_xml_by_id'),

    # AUTH
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
