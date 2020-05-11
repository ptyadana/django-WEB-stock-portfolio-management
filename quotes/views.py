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

def search_stock_batch(base_url, stock_tickers):
    try:
        token = settings.IEXCLOUD_TEST_API_TOKEN
        url = base_url + stock_tickers + '&types=quote&token=' + token
        print(f'url: {url}')
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
        else:
            data = {'Error' : 'There has been an unexpected issues. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data

def check_valid_stock_ticker(ticker):
    base_url = 'https://sandbox.iexapis.com/stable/stock/'
    stock = search_stock(base_url, ticker)
    if 'Error' not in stock:
        return True
    return False

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
        ticker = request.POST['ticker']
        if ticker:
            form = StockForm(request.POST or None)
            if form.is_valid():
                if check_valid_stock_ticker(ticker):
                    form.save()
                    messages.success(request, f'{ticker} has been added successfully.')
                    return redirect('portfolio')

        messages.warning(request, 'Please enter a valid ticker name.')
        return redirect('portfolio')
    else:
        stocks = Stock.objects.all()
        if stocks:
            ticker_list = [stock.ticker for stock in stocks]
            ticker_list = list(set(ticker_list))
            
            tickers = ','.join(ticker_list)
            base_url = 'https://sandbox.iexapis.com/stable/stock/market/batch?symbols='
            data = search_stock_batch(base_url, tickers)
            print(data)

        return render(request, 'quotes/portfolio.html', {'stocks':stocks, 'data':data})

def delete_stock(request, stock_id):
    stock = Stock.objects.get(pk=stock_id)
    stock.delete()

    messages.success(request, f'{stock.ticker} has been deleted successfully.')
    return redirect('portfolio')


if __name__ == "__main__":
    pass
    # base_url = 'https://sandbox.iexapis.com/stable/stock/'
    # stock_ticker = 'IBM'
    # data = search_stock(base_url, stock_ticker)