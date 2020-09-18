from django.contrib import admin
from .models import User, AuctionListing, Comments, Bids


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
admin.site.register(Comments)
admin.site.register(Bids)
