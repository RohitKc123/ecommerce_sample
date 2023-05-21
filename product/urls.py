from django.urls import path
from .views import product_add, product_list, add_to_wishlist, delete_order, update_price, category_filter, \
    filterby_company, filterby_price, search_form, email_send, about_page, checkout, khaltirequest_confirm, \
    khalti_verify, product_description, featured_product_page, latest_product_page

urlpatterns = [
    path('add/', product_add),
    path('', product_list, name="item_list"),
    path('wishlist/', add_to_wishlist, name='user_wishlist'),
    path('delete/<int:id>/<int:quantity>/', delete_order, name='delete_item'),
    path('update_price/<int:id>/', update_price, name='update_price'),
    path('filter-product/<str:category>/', category_filter, name="filter_product"),
    path('filter-product-company/<str:category>/<str:company>/', filterby_company),
    path('filter-product-price/<str:category>/<str:company>/<str:price>/', filterby_price),
    path('search/', search_form),
    path('email-sent/<int:id>/<int:itemid>/<int:quantity>/<int:price>/', email_send),
    path('about/', about_page),
    path('checkout/', checkout),
    path('khalti/<int:id>/', khaltirequest_confirm, name="khaltirequest"),
    path('khalti-verify/', khalti_verify),
    path('product-description/<int:id>/', product_description),
    path('featured_product/', featured_product_page),
    path('latest-product/', latest_product_page)
]
