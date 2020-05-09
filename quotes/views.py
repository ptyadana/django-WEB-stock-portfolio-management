from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'quotes/home.html')

def about(request):
    return render(request, 'quotes/about.html')