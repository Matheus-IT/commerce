from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ''' Use the properties and methods of AbstractUser '''
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.CharField(max_length=1024, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=32)

    CATEGORY_LABELS = ('Fashion', 'Toys', 'Electronics', 'Home')
    CATEGORY_VALUES = ('fashion', 'toys', 'electronics', 'home')
    
    CATEGORY_CHOICES = list(zip(CATEGORY_LABELS, CATEGORY_VALUES))
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    content = models.CharField(max_length=1024)
    commentAuthor = models.CharField(max_length=32)
    
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
    pass
