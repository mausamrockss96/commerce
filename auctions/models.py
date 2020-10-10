from django.contrib.auth.models import AbstractUser
from django.db import models

    
class User(AbstractUser):
    pass

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=2000)
    startingbid = models.IntegerField()
    highestbid = models.IntegerField()
    image = models.URLField(blank=True)
    category = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="wishedby")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="wisheditem")
    
    def __str__(self):
        return f"{self.user} wishes to buy {self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="commented_on")
    comment = models.CharField(max_length=2000)

    def __str__(self):
        return f"{self.user} on {self.listing} says {self.comment}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="item")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="bidder")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.user} bids an amount of {self.bid} on {self.listing}" 
