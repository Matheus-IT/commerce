from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('create/', views.createListing, name='createListing'),
    path('listings/<int:listingId>', views.ListingPage.as_view(), name='listingPage'),
    path('categories/', views.categoriesPage, name='categories')
]
