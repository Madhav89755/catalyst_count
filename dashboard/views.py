from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login_page')
def upload_data(request):
    return render(request, 'upload_data.html')

@login_required(login_url='login_page')
def query_builder(request):
    return render(request, 'query_builder.html')
