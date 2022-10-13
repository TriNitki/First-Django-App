from django.shortcuts import render

def index(request):
    '''Home page of Learning Log'''
    return render(request, 'learning_logs/index.html')