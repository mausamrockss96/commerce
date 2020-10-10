from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User,Listing,Wishlist,Comment,Bid

def index(request):
    listings = Listing.objects.all()
    if listings is None:
        return render(request, "auctions/index.html",{
        "active":False
    })
    return render(request, "auctions/index.html",{
        "active":listings
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

@login_required(login_url='/')
def newlisting(request):
    if request.method == "POST":
        owner = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        startingbid = request.POST.get("startingbid")
        image = request.POST.get("image")
        category = request.POST.get("category")
        new_listing = Listing(owner = owner,title=title,description=description,startingbid=startingbid,highestbid=startingbid,image=image,category=category)
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/newlisting.html")

@login_required(login_url='/')
def listing(request,id):
    listing = Listing.objects.get(id = id)
    userwish = Wishlist.objects.filter(user=request.user).values('listing_id')

    wishlist = []
    for content in userwish:
        wishlist.append(content['listing_id'])
    if id in wishlist:
        boolean = True
    else:
        boolean = False
    comments = Comment.objects.filter(listing = listing).values('id')
    comment_list = []
    for content in comments:
        comment = Comment.objects.get(id = content['id'])
        comment_list.append(comment)
    print(comment_list)

    if request.method == "POST":
        bid = request.POST.get("newbid")
        newbid = Bid(listing = listing, user = request.user, bid = bid)
        newbid.save()
        listing.highestbid = bid
        listing.save()
        
    if listing.status:
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "user":request.user,
            "wishlist":boolean,
            "comments":comment_list
        })
    else:
        count = Bid.objects.filter(listing = listing).count()
        if count==0:
            winner = None
        else:
            price = Bid.objects.filter(listing = listing).aggregate(Max('bid'))
            price = price.get('bid__max')
            user = Bid.objects.filter(listing = listing, bid=price).first()
            winner = user.user
        
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "user":request.user,
            "wishlist":boolean,
            "comments":comment_list,
            "winner":winner
        })

@login_required(login_url='/')
def wishlist(request):
    user = request.user
    listings = Wishlist.objects.filter(user=user).values('listing_id')
    wishlist = []
    for listing in listings:
            wish = Listing.objects.get(id = listing['listing_id'])
            wishlist.append(wish)
    print(wishlist)
    if wishlist is None:
        return render(request, "auctions/wishlist.html",{
        "wishlist":False
    })
    print("HERE")
    return render(request, "auctions/wishlist.html",{
        "wishlist":wishlist
    })

@login_required(login_url='/')
def alterwish(request,id):
    user = request.user
    listing = Listing.objects.get(id=id)
    if Wishlist.objects.filter(user=user,listing=listing).exists():
        wish = Wishlist.objects.get(user=user,listing=listing)
        wish.delete()
        return HttpResponseRedirect(reverse("listing", args=(),
            kwargs={'id': id}))
    else:
        wish = Wishlist(user=user,listing=listing)
        wish.save()
        return HttpResponseRedirect(reverse("listing", args=(),
            kwargs={'id': id}))


@login_required(login_url='/')
def comment(request,id):
    user = request.user
    listing = Listing.objects.get(id = id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        new_comment = Comment(user = user, listing=listing,comment=comment)
        new_comment.save()
    
    return HttpResponseRedirect(reverse("listing", args=(),
            kwargs={'id': id}))


@login_required(login_url='/')
def close(request,id):
    listing = Listing.objects.get(id = id)
    listing.status = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(),
        kwargs={'id': id}))

@login_required(login_url='/')
def categories(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html")
    else:
        category = request.POST["category"]
        listings = Listing.objects.filter(category = category)
        if len(listings) > 0:
            boolean = True
        else:
            boolean = False
        print(category)
        return render(request, "auctions/categories.html", {
            "active":listings,
            "boolean" : boolean
            })