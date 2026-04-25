from django.shortcuts import render, redirect
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

def api_docs(request):
    return render(request, 'api_docs.html')

def redirect_api(request):
    return redirect('api_docs')