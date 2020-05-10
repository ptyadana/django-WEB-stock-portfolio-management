from django.urls import path

from .views import home,about,add_stock,delete_stock

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('addstock/', add_stock, name='add_stock'),
    path('deletestock/<int:stock_id>', delete_stock, name='delete_stock'),
]
