from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ''' Use the properties and methods of AbstractUser '''
    pass


class Comments(models.Model):
    content = models.CharField(max_length=120)

    def __str__(self):
        return f'Content: {self.content}'


class Bids(models.Model):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=120)
    currentPrice = models.DecimalField(max_digits=10, decimal_places=2)
    imageUrl = models.CharField(max_length=1024, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    comments = models.ForeignKey(
        Comments, 
        on_delete=models.CASCADE, 
        blank=True,
        null=True,
        related_name='auction'
    )

    CATEGORY_CHOICES = [
        ('Fashion', 'fashion'),
        ('Toys', 'toys'),
        ('Electronics', 'electronics'),
        ('Home', 'home')
    ]
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return f'{self.title}'
