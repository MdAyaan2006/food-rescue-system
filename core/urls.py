from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('feed/', views.food_feed, name='feed'),
    path('create/', views.create_listing, name='create_listing'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    # NEW DELETE URL
    path('delete/<int:listing_id>/', views.delete_listing, name='delete_listing'),
    
    path('claim/<int:listing_id>/', views.claim_listing, name='claim_listing'),
    path('contact/', views.contact_us, name='contact'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]