from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib import messages

import requests
import json

from .models import Stock
from .forms import StockForm


def search_stock(base_url, stock_ticker):
    try:
        token = settings.IEXCLOUD_TEST_API_TOKEN
        url = base_url + stock_ticker + '/quote?token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
        else:
            data = {'Error' : 'There was a problem with your provided ticker symbol. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data
   
def home(request):
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        base_url = 'https://sandbox.iexapis.com/stable/stock/'
        stocks = search_stock(base_url, stock_ticker)
        return render(request, 'quotes/home.html', {'stocks':stocks})
    return render(request, 'quotes/home.html')

def about(request):
    return render(request, 'quotes/about.html')

def portfolio(request):
    if request.method == 'POST':
        if request.POST['ticker']:
            form = StockForm(request.POST or None)

            if form.is_valid():
                form.save()
                messages.success(request, 'stock has been added successfully.')
        else:
            messages.warning(request, 'Please enter ticker name.')
        return redirect('portfolio')
    else:
        stocks = Stock.objects.all()
        return render(request, 'quotes/portfolio.html', {'stocks':stocks})

def delete_stock(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    stock.delete()

    messages.success(request, 'stock has been deleted successfully.')
    return redirect('portfolio')


if __name__ == "__main__":
    base_url = 'https://sandbox.iexapis.com/stable/stock/'
    stock_ticker = 'IBM'

    data = connect(base_url, stock_ticker)