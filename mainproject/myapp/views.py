from django.shortcuts import render
#from django.views.decorators.cache import never_cache

# Create your views here.
#@never_cache
def index(request):
    return render(request,'index.html')
