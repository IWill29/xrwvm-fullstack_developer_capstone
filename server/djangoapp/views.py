# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


@csrf_exempt
def logout_request(request):
    """
    Logs out current user. Accepts GET or POST.
    Returns JSON with status 200 on success.
    """
    try:
        if request.method not in ("GET", "POST"):
            return JsonResponse({"error": "Method not allowed"}, status=405)
        logout(request)
        logger.info("User logged out: %s", request.user or "anonymous")
        return JsonResponse({"detail": "logged out"}, status=200)
    except Exception:
        logger.exception("Logout error")
        return JsonResponse({"error": "server error"}, status=500)


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    try:
        data = json.loads(request.body.decode("utf-8"))
        username = data.get("userName") or data.get("username")
        password = data.get("password")
        first = data.get("firstName", "")
        last = data.get("lastName", "")
        email = data.get("email", "")
        if not username or not password:
            return JsonResponse({"error":"username and password required"}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error":"user exists"}, status=400)
        user = User.objects.create_user(username=username, password=password, email=email, first_name=first, last_name=last)
        user.save()
        login(request, user)
        return JsonResponse({"userName": username}, status=201)
    except Exception:
        logger.exception("Registration error")
        return JsonResponse({"error":"server error"}, status=500)

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...
