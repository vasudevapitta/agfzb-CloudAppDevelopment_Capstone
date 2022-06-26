from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def get_about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    print("Login Request")
    if request.method == "POST":
        username = request.POST['usernameLoginField']
        print("Login: Username", username)
        password = request.POST['passwordLoginField']
        print("Login: Password", password)
        user = authenticate(username=username, password=password)
        if user is not None:
            print("Login: User", User)
            login(request, user)
            return redirect("djangoapp:index")

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    if request.method == "POST":
        logout(request)
        return redirect("djangoapp:index")

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    print("Registartion Request")
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    if request.method == "POST":
        username = request.POST['usernameField']
        firstName = request.POST['firstNameField']
        lastName = request.POST['lastNameField']
        password = request.POST['passwordField']
        userResult = User.objects.filter(username=username)
        if len(userResult) == 0:
            user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName, password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    print("Index Request")
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

