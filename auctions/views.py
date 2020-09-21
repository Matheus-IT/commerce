from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db import IntegrityError

from .models import *


def index(request):
    return render(request, 'auctions/index.html', {
        'auctionListings': AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == 'POST':
        from django.contrib.auth.models import User
        
        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return render(request, 'auctions/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auctions:index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'auctions/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'auctions/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('auctions:index'))
    else:
        return render(request, 'auctions/register.html')


def createListing(request):
    if request.method == 'POST':
        # try to create a new auction listing
        title = request.POST['title']
        description = request.POST['description']
        currentPrice = request.POST['initialPrice']
        
        # validate the ones that are not required
        imageUrl = request.POST['imageUrl']
        if not imageUrl:
            imageUrl = ''
        
        category = request.POST['categories']
        if not category:
            category = ''

        try:
            auctionListing = AuctionListing.objects.create(
                title=title,
                description=description,
                currentPrice=currentPrice,
                imageUrl=imageUrl,
                category=category
            )
            auctionListing.save()
        except IntegrityError:
            return render(request, 'auctions/createListing.html', {
                # give category choices as context to the select
                'categoryChoices': AuctionListing.CATEGORY_CHOICES,
                'message': 'Something went wrong when trying to create a new auction listing... Try again'
            })
        else:
            return HttpResponseRedirect(reverse('auctions:index'))
    elif User.is_authenticated:
        return render(request, 'auctions/createListing.html', {
            # give category choices as context to the select
            'categoryChoices': AuctionListing.CATEGORY_CHOICES
        })

def listingPage(request, listingId):
    auctionListing = AuctionListing.objects.filter(id=listingId)[0]

    return render(request, 'auctions/listingPage.html', { 'listing': auctionListing })
