from django.contrib.auth.models import AbstractUser
from django.db import models

USERNAME_LENGTH = 32

class User(AbstractUser):
    ''' Use the properties and methods of AbstractUser '''
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2)
    lasBidAuthor = models.CharField(max_length=USERNAME_LENGTH)
    imageUrl = models.CharField(max_length=1024, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=USERNAME_LENGTH)

    CATEGORY_VALUES = ('fashion', 'toys', 'electronics', 'home')
    CATEGORY_LABELS = ('Fashion', 'Toys', 'Electronics', 'Home')
    
    CATEGORY_CHOICES = list(zip( CATEGORY_VALUES, CATEGORY_LABELS))
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    content = models.CharField(max_length=1024)
    commentAuthor = models.CharField(max_length=USERNAME_LENGTH)
    
    auction = models.ForeignKey(
        AuctionListing,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments'
    )

    def __str__(self):
        return f'Content: {self.content}'


class Bid(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
    bidAuthor = models.CharField(max_length=USERNAME_LENGTH)
    
    auction = models.ForeignKey(
        AuctionListing,
        on_delete=models.CASCADE, 
        related_name='bids'
    )

    def __str__(self):
        return f'Value: {self.value} Bid author: {self.bidAuthor}'
