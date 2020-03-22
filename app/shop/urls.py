from django.urls import path
from shop import views


urlpatterns = [
    path('', views.StartPageTemplateView.as_view(), name='start_page_url'),
    path('books/', views.BookListView.as_view(), name='book_list_url'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail_url'),
    path('rewiew/<int:pk>/', views.RewiewView.as_view(), name='add_rewiew_url'),
]
