from django.urls import path

from .views import home,about,portfolio,delete_stock

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('portfolio/', portfolio, name='portfolio'),
    path('deletestock/<int:stock_id>', delete_stock, name='delete_stock'),
]
