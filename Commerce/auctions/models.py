from django.contrib.auth.models import AbstractUser
#this is for the login
from django.db import models


class User(AbstractUser):
    pass
    #just passssss

class Bid(models.Model):
    #each model is like a table, and is a subclass of models.Model, and all of the following attributes of the table are fields storing your data
    bid = models.IntegerField(default = 0)
    #integerfields for numbers
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "bid")
    #foreign key is a link/address/reference to a different table. It is not the data itself!!  
    def __str__(self):
        return f"Bid of {self.bid} from {self.user}"
        #This is what is shown to the django admin

class AuctionListings(models.Model):
    name_of_item = models.CharField(max_length=32)
    description = models.CharField(max_length=400)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name="auctionlistings", default = None)
    #reference to the user table, if the user is deleted then the auction listing is deleted, related name specifies how to find this data from the user table (in reverse).
    #default is equal to None in case owner isn't submitted/errors
    bid = models.ForeignKey(Bid, on_delete = models.CASCADE, related_name = "auctionlistings", default = None)
    is_closed = models.BooleanField(default=False, blank=True, null=True)
    url = models.CharField(max_length=800)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    category = models.CharField(max_length=50)

    #if you want to add date of the auction listing, you can do that without putting it in the form.
    """
    date_created = models.DateTimeField(auto_now_add=True, auto_now = False, blank=True)
    #"auto_now_add=True" is if you want the date when the entry is added
    #"auto_now=True" is if you want the date when the entry is last updated
    might come in useful
    """
    def __str__(self): 
        return f"{self.name_of_item}: {self.bid}"


class Comments(models.Model):
    text = models.CharField(max_length=800)
    writer = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    listing = models.ForeignKey(AuctionListings, on_delete = models.CASCADE, related_name = "comments")