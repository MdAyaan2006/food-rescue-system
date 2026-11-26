from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .forms import CustomUserCreationForm, FoodListingForm, ContactForm, UserProfileForm
from .models import FoodListing, User

def home(request):
    total_kg = FoodListing.objects.filter(is_claimed=True).aggregate(Sum('quantity_kg'))['quantity_kg__sum'] or 0
    total_meals = int(total_kg * 2)
    return render(request, 'core/home.html', {'total_kg': total_kg, 'total_meals': total_meals})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def food_feed(request):
    listings = FoodListing.objects.filter(is_claimed=False).order_by('-created_at')
    return render(request, 'core/feed.html', {'listings': listings})

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = FoodListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.donor = request.user
            listing.save()
            return redirect('feed')
    else:
        form = FoodListingForm()
    return render(request, 'core/create_listing.html', {'form': form})

@login_required
def claim_listing(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id)
    if request.method == 'POST' and not listing.is_claimed:
        listing.is_claimed = True
        listing.claimed_by = request.user
        listing.save()
    return redirect('feed')

@login_required
def profile(request):
    donations = FoodListing.objects.filter(donor=request.user).order_by('-created_at')
    claims = FoodListing.objects.filter(claimed_by=request.user).order_by('-created_at')
    return render(request, 'core/profile.html', {'donations': donations, 'claims': claims})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

# NEW: Delete listing logic
@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(FoodListing, id=listing_id, donor=request.user)
    if request.method == 'POST':
        listing.delete()
    return redirect('profile')

def contact_us(request):
    success = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()
    else:
        initial_data = {'name': request.user.username, 'email': request.user.email} if request.user.is_authenticated else {}
        form = ContactForm(initial=initial_data)
    return render(request, 'core/contact.html', {'form': form, 'success': success})

def leaderboard(request):
    top_donors = User.objects.filter(user_type='DONOR', donations__is_claimed=True).annotate(
        total_donated=Sum('donations__quantity_kg')
    ).order_by('-total_donated')[:10]
    return render(request, 'core/leaderboard.html', {'top_donors': top_donors})