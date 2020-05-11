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
    data_list = []

    try:
        token = settings.IEXCLOUD_TEST_API_TOKEN
        url = base_url + stock_tickers + '&types=quote&token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
            for item in data:
                data_list.append(data[item]['quote'])
        else:
            data = {'Error' : 'There has been an unexpected issues. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data_list

def check_valid_stock_ticker(stock_ticker):
    base_url = 'https://sandbox.iexapis.com/stable/stock/'
    stock = search_stock(base_url, stock_ticker)
    if 'Error' not in stock:
        return True
    return False

def check_stock_ticker_existed(stock_ticker):
    try:
        stock = Stock.objects.get(ticker=stock_ticker)
        if stock:
            return True
    except Exception:
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
                if check_stock_ticker_existed(ticker):
                    messages.warning(request, f'{ticker} is already existed in Portfolio.')
                    return redirect('portfolio')

                if check_valid_stock_ticker(ticker):
                    #add stock                    
                    form.save()
                    messages.success(request, f'{ticker} has been added successfully.')
                    return redirect('portfolio')

        messages.warning(request, 'Please enter a valid ticker name.')
        return redirect('portfolio')
    else:
        stockdata = Stock.objects.all()
        if stockdata:
            ticker_list = [stock.ticker for stock in stockdata]
            ticker_list = list(set(ticker_list))
            
            tickers = ','.join(ticker_list)
            base_url = 'https://sandbox.iexapis.com/stable/stock/market/batch?symbols='
            stockdata = search_stock_batch(base_url, tickers)
        else:
            messages.info(request, 'Currently, there are no stocks in your portfolio!')
        return render(request, 'quotes/portfolio.html', {'stockdata':stockdata})

def delete_stock(request, stock_symbol):
    stock = Stock.objects.get(ticker=stock_symbol)
    stock.delete()

    messages.success(request, f'{stock.ticker} has been deleted successfully.')
    return redirect('portfolio')