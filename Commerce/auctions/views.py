from django.contrib.auth import authenticate, login, logout
#This is for logging the user in later
from django.db import IntegrityError
#This makes sure there isn't a repeated user
from django.http import HttpResponse, HttpResponseRedirect
#Returns http response
from django.shortcuts import render
#renders the page by going to the template
from django.urls import reverse
#uses the url to find the path to the view which goes to the template
from .models import User, Bid, AuctionListings, Comments
#!you import all the models that you created. Common mistake is when you created a new model but you didn't put it here or you didn't migrate. 
#(At least for me)
def create_listing(request):
    return render(request, "auctions/create_listing.html")
#Goes to the form page

def submit_listing(request):
    if request.method == "POST":
        name_of_item = request.POST['name_of_item']
        user = request.user 
        description = request.POST['description']
        category = request.POST['category']
        image_url = request.POST['image_url']
        bid = Bid(bid=int(request.POST["bid"]), user=user)
        bid.save()
        #you save the bid after you create it. This basically adds an "row" to the "table" for that specific model. 
        listing = AuctionListings(name_of_item=name_of_item, description=description, owner=user, bid = bid, is_closed = False, url = image_url, category = category)
        listing.save()
        #!You relate it to bid by saving bid=bid, bid is a foreignKey so it knows that it is linked to that specific bid in the other model.
        return HttpResponseRedirect(reverse("index"))
        #User is returned to the index page
    return render(request, "auctions/create_listing.html")
    #or else they are asked to retry to create a listing.

def index(request):
    active_listings = AuctionListings.objects.filter(is_closed=False)
    #You only show those that are filtered. You can give the table a Boolean value "is closed for this"
    return render(request, "auctions/index.html",{
            "active_listings": active_listings
        })

def category(request):
    if request.method == "POST":
        chosen_category = request.POST["category"]
        active_listings = AuctionListings.objects.filter(is_closed=False,category=chosen_category)
        #!Here you filter out everything not in that specific category
    return render(request, "auctions/index.html",{
            "active_listings": active_listings
        })

def display_listing(request, active_listings_id):
    #!common error here is that listing id is turned into a listing_id instead of listing.id on the templates. This is because the url doesn't accept "."
    listing = AuctionListings.objects.get(pk=active_listings_id)
    #You get that specific listing from the table by giving that specific id, this should be returned along with the url.
    comments = listing.comments.all()
    #gets all of the comments
    if request.user == listing.owner:
        is_owner = True
    #this asks if the user is viewing the page is the owner of the auction, if it is we allow the owner to have certain privelidges
    #, thus we have a if statement on the template page that asks the user if they are the owner and show things accordingly.
    else: 
        is_owner = False
    is_listing_in_watchlist = request.user in listing.watchlist.all()
    #This is used for whether the watchlist button says "remove from watchlist" or "add to watchlist"
    return render(request,"auctions/display_listing.html",{
        "listing": listing,
        "comments": comments,
        "is_owner": is_owner,
        "is_listing_in_watchlist": is_listing_in_watchlist
        })


def new_bid(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    new_bid = bid = int(request.POST["new_bid"])
    current_bid = listing.bid.bid 
    #Here we crossreference by using the foreign key. Here we go into the listings, 
    #find that specific listing then find the foreign key "bid" that references to another table containing the specific "bid" that we need
    #so we have listing.bid.bid.

    if new_bid > current_bid:
        updated_bid = Bid(bid = new_bid, user=request.user)
        updated_bid.save()
        listing.bid = updated_bid
        listing.save()
        return render(request,"auctions/display_listing.html", {
            "listing":listing,
            "message":"Your Bid was added successfully.",
            "updated": True,
            })
    else:
        return render(request,"auctions/display_listing.html",{
            "listing":listing,
            "message":"Sorry, your bid was not bigger than the latest bid.",
            "updated": False,
            })


def add_watchlist(request,listing_id):
    user = request.user
    listing = AuctionListings.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("display_listing",args=(listing_id,)))

def remove_watchlist(request,listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    user = request.user
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("display_listing",args=(listing_id,)))


def close_auction(request, listing_id):
    listing = AuctionListings.objects.get(pk=listing_id)
    listing.is_closed = True
    listing.save()
    return HttpResponseRedirect(reverse("display_listing", args=(listing_id, )))

def add_comment(request, listing_id):
    if request.method == "POST":
        user = request.user
        text = request.POST["comment"]
        listing = AuctionListings.objects.get(pk=listing_id)
        new_comment = Comments(text=text, writer=user, listing=listing)
        new_comment.save()
        return HttpResponseRedirect(reverse("display_listing",args=(listing_id,)))

def watchlist(request):
    user = request.user
    users_watchlist_of_items = user.watch_listings.all()
    return render(request, "auctions/watchlist.html",{
        "users_watchlist_of_items" : users_watchlist_of_items
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
