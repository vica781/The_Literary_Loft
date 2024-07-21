from django.shortcuts import render

# Create your views here.

def index(request):
    """ A view that displays the index page """    
    return render(request, 'books/index.html')

def about(request):
    """ A view that displays the about page """
    return render(request, 'books/about.html')

def contact(request):
    """ A view that displays the contact page """
    return render(request, 'books/contact.html')
