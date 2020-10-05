from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from django.db import IntegrityError

from .models import *


def index(request):
    if 'watchlist' not in request.session:
        request.session['watchlist'] = []
    
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
        author = request.user.username
        
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
                author=author,
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


def closeListing(request, listingId):
    listing = AuctionListing.objects.get(pk=listingId)

    if listing.lastBidAuthor:
        try:
            winner = User.objects.get(username=listing.lastBidAuthor)
            listing.isClosed = True
            listing.save()
            
            try:
                # verify if the item is already inside the watchlist
                closedListing = winner.watchlistItems.get(auction_id=listing.id)
            except:
                closedListing = winner.watchlistItems.create(auction=listing, user=winner)
                closedListing.save()

            msg = f'The winner is {winner.username}, {listing} was closed!'
        except Exception as exc:
            msg = exc
    else:
        listing.delete()
        msg = f'There\'s no winner, the listing was deleted!'

    print(msg)

    return render(request, 'auctions/closeListing.html', { 'mensagem': msg })


class ListingPage(View):
    from .forms import AddBidForm, AddCommentForm

    template_name = 'auctions/listingPage.html'

    def _getForm(self, request, formClass, prefix):
        data = request.POST if prefix in request.POST else None
        return formClass(data, prefix=prefix)

    def verifyItemInWatchlist(self, watchlist, listingId):
        for item in watchlist:
            if listingId == item.auction_id:
                return True
        return False

    def get(self, request, listingId):
        auctionListing = AuctionListing.objects.get(id=listingId)
        currentUser = request.user.username

        isInWatchlist = self.verifyItemInWatchlist(request.user.watchlistItems.all(), listingId)

        return render(request, self.template_name, {
            'listing': auctionListing,
            'BidForm': self.AddBidForm(),
            'CommentForm': self.AddCommentForm(),
            'currentUser': currentUser,
            'listingIsInWatchlist': isInWatchlist
        })

    def post(self, request, listingId):
        auctionListing = AuctionListing.objects.get(id=listingId)

        BidForm = self._getForm(request, self.AddBidForm, prefix=self.AddBidForm.prefix)
        CommentForm = self._getForm(request, self.AddCommentForm, prefix=self.AddCommentForm.prefix)

        currentUser = request.user.username

        additionalErrorMessage = ''

        if CommentForm.is_valid() and CommentForm.is_bound:
            # create a new comment
            newCommentContent = CommentForm.cleaned_data['newCommentValue']

            try:
                newComment = Comment.objects.create(
                    content=newCommentContent,
                    commentAuthor=currentUser,
                    auction=auctionListing
                )

                newComment.save()
                
                CommentForm = self.AddCommentForm()
            except Exception as err:
                print(err)
        elif BidForm.is_valid() and BidForm.is_bound:
            newBidContent = BidForm.cleaned_data['newBidValue']

            if newBidContent > auctionListing.currentPrice:
                # post new bid
                try:
                    newBid = Bid.objects.create(
                        value = newBidContent,
                        bidAuthor=currentUser,
                        auction=auctionListing
                    )
                    
                    auctionListing.currentPrice = newBid.value
                    auctionListing.lastBidAuthor = currentUser

                    auctionListing.save()
                    newBid.save()
                    
                    BidForm = self.AddBidForm()
                except Exception as err:
                    print(err)
            else:
                additionalErrorMessage = """
                    <ul class="errorlist">
                        <li><strong>The bid should be greater than the current price</strong></li>
                    </ul>
                """
        else:
            print('Something went wrong...')

        return render(request, self.template_name, {
            'listing': auctionListing,
            'BidForm': BidForm,
            'currentUser': currentUser,
            'CommentForm': CommentForm,
            'additionalErrorMessage': additionalErrorMessage
        })


def categoriesPage(request):
    filteredAuctionListings = []
    
    if request.method == 'POST':
        categoryChosen = request.POST['categories']

        filteredAuctionListings = AuctionListing.objects.filter(category=categoryChosen)

    categoryChoices = AuctionListing.CATEGORY_CHOICES
    
    return render(request, 'auctions/categories.html', {
        'categoryChoices': categoryChoices,
        'filteredAuctionListings': filteredAuctionListings
    })


def watchlistPage(request):
    watchlist = request.user.watchlistItems.all()
    
    return render(request, 'auctions/watchlist.html', { 'watchlist': watchlist })


def watchlistToggle(request, listingId):
    from django.core.exceptions import ObjectDoesNotExist
    
    watchlistItems = request.user.watchlistItems
    auction = AuctionListing.objects.get(pk=listingId)

    try:
        # if there's already a watchlist item corresponding to the
        # current listing
        item = watchlistItems.get(auction_id=listingId)
        item.delete()
    except ObjectDoesNotExist:
        try:
             newItem = watchlistItems.create(auction=auction, user=request.user)
             newItem.save()
        except Exception as err:
             print(err)
    finally:    
        return HttpResponseRedirect(reverse('auctions:watchlistPage'))
