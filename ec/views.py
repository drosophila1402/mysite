from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'ec/index.html', {})
    
def test(request):
    return render(request, 'base/test.html', {})