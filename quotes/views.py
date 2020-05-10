from django.shortcuts import render
from django.conf import settings

import pathlib
import requests
import json

def connect(base_url, stock_ticker):
    try:
        token = settings.IEXCLOUD_TEST_API_TOKEN
        url = base_url + stock_ticker + '/quote?token=' + token
        data = requests.get(url)

        if data.status_code == 200:
            data = json.loads(data.content)
        else:
            data = {'Error' : 'There is an error with the provided ticker. Please try again'}
    except Exception as e:
        data = {'Error':'There has been some connection error. Please try again later.'}
    return data
   
def home(request):
    if request.method == 'POST':
        stock_ticker = request.POST['stock_ticker']
        base_url = 'https://sandbox.iexapis.com/stable/stock/'
        stocks = connect(base_url, stock_ticker)
        return render(request, 'quotes/home.html', {'stocks':stocks})
    return render(request, 'quotes/home.html')

def about(request):
    return render(request, 'quotes/about.html')

if __name__ == "__main__":
    base_url = 'https://sandbox.iexapis.com/stable/stock/'
    stock_ticker = 'IBM'

    data = connect(base_url, stock_ticker)