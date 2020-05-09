from django.urls import path

from .views import home,about

urlpatterns = [
    path('', home, name='home'),
    path('quotes/', home, name='home'),
    path('about/', about, name='about'),
]
