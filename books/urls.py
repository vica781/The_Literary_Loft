from django.urls import path
from . import views

app_name = 'books'  

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Book-related URLs
    path('books/', views.book_list, name='book_list'),  # Generic book list (all books)
    path('books/subcategory/<slug:subcategory_slug>/', views.book_list, name='book_list_by_subcategory'),  # Subcategory-specific
    path('books/<slug:category_slug>/', views.book_list, name='book_list_by_category'),  # Category-specific
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('book_list/', views.book_list, name='book_list_alt'),  # Alternative for listing all books
]
