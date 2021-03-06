from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('create/', views.createListing, name='createListing'),
    path('close/<int:listingId>', views.closeListing, name='closeListing'),
    path('delete/<int:listingId>', views.deleteListing, name='deleteListing'),

    path('listings/<int:listingId>', views.ListingPage.as_view(), name='listingPage'),
    path('categories/', views.categoriesPage, name='categories'),
    path('watchlist/', views.watchlistPage, name='watchlistPage'),
    path('watchlistToggle/<int:listingId>', views.watchlistToggle, name='watchlistToggle')
]
