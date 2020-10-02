from django.contrib import admin
from .models import User, AuctionListing, WatchlistItem, Comment, Bid


class AuctionListingAdmin(admin.ModelAdmin):
	list_display = (
		'id', 
		'title',  
		'currentPrice',  
		'createdAt',  
		'category'
	)


# Register your models here.
admin.site.register(User)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(WatchlistItem)
admin.site.register(Comment)
admin.site.register(Bid)
