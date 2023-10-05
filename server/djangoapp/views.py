from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    context = {}
    print("user `{}` logged out successfully".format(request.user.username))
    context['message'] = "user logged out"
    logout(request)
    return render(request, 'djangoapp/index.html', context)
# ...

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("{} is a new user".format(username))
        
        if not user_exist:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return render(request, 'djangoapp/registration.html', context)
        else:
            return render(request, 'djangoapp/registration.html', context)


    
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/1d24272f-6771-49cf-9a2e-9c5f72c0702e/default/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        context = {}
        context["dealerships_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


# def get_dealerships_by_id(request):
#     if request.method == "GET":
#         url = "https://us-south.functions.appdomain.cloud/api/v1/web/1d24272f-6771-49cf-9a2e-9c5f72c0702e/default/get-dealership"
#         dealerships = get_dealer_by_id(url, dealerId)
#         context = {}
#         context["dealerships_list"] = dealerships
#         return render(request, 'djangoapp/index.html', context)




# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealerId):
    if request.method == "GET":
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/1d24272f-6771-49cf-9a2e-9c5f72c0702e/default/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, dealerId)
        context = {}
        context['dealer'] = dealer


        reviews_url = "https://us-south.functions.appdomain.cloud/api/v1/web/1d24272f-6771-49cf-9a2e-9c5f72c0702e/default/get-review"
        reviews = get_dealer_reviews_from_cf(reviews_url, dealerId)
        context = {}
        context['reviews'] = reviews 
        return render(request, 'djangoapp/dealer_details.html', context)
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

