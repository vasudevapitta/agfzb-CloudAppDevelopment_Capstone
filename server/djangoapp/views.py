from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import post_request, get_dealers_from_cf, get_dealer_reviews_from_cf, get_dealer_by_id
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
    context = dict()
    if request.method == "GET":
        url = "https://630f2802-ef1e-4b85-80eb-a1d6f6e2644b-bluemix.cloudantnosqldb.appdomain.cloud/api/dealership?state=\"\""
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        context["result"] = result
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        context=dict()
        url = "https://630f2802-ef1e-4b85-80eb-a1d6f6e2644b-bluemix.cloudantnosqldb.appdomain.cloud"
        dealer_url = url + "/api/dealership"
        review_url = url + "/api/review"

        dealer, dealer_status = get_dealer_by_id(dealer_url, dealer_id)
        context["dealer"] = dealer
        context["dealer_result"] = dealer_status

        reviews, review_status = get_dealer_reviews_from_cf(review_url, dealer_id)
        context["reviews"]=reviews
        context["review_result"]=review_status

        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        context = dict()
        url = "https://630f2802-ef1e-4b85-80eb-a1d6f6e2644b-bluemix.cloudantnosqldb.appdomain.cloud"

        dealer, dealer_status = get_dealer_by_id(url, dealer_id)
        context["dealer"] = dealer
        context["result"] = dealer_status
        cars = CarModel.objects.all().filter(dealer_id=dealer_id)
        context["cars"] = cars
        context["dealer_id"] = dealer_id
        return render(request, "djangoapp/add_review.html", context)

    elif request.method == "POST":
        if request.user.is_authenticated:
            url = "https://630f2802-ef1e-4b85-80eb-a1d6f6e2644b-bluemix.cloudantnosqldb.appdomain.cloud"
            review = dict()
            review["name"] = request.user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = True if (request.POST.get('purchasecheck', "False") == "on") else False
            car_id = request.POST.get("car", None)
            if car_id != None:
                car = CarModel.objects.get(id=car_id)
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"] = int(car.yearpublished())
                review["purchase_date"] = request.POST["purchasedate"]
                     
            json_payload = dict()
            json_payload["review"] = review
            result, status_code = post_request(url, json_payload, dealer_id = dealer_id)
            print(result)

            if (result.get('message') == "ok"):
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
            else:
                context=dict()
                context["error"] = result["message"]
                return render(request, 'djangoapp/add_review.html', context)
        else:    
            context=dict()
            context["error"] = "User is not authenticated"
            url = "https://630f2802-ef1e-4b85-80eb-a1d6f6e2644b-bluemix.cloudantnosqldb.appdomain.cloud"
            dealer, dealer_status = get_dealer_by_id(url, dealer_id)
            context["dealer"] = dealer
            context["result"] = dealer_status
            context["dealer_id"] = dealer_id
            cars = CarModel.objects.all().filter(dealer_id = dealer_id)
            
            return render(request, "djangoapp/add_review.html", context)
