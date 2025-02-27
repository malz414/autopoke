from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm  # If using the custom form
from .models import Pokemon, Item, Synergy
from django.db.models import Q  # For filtering
from django.http import JsonResponse

def search_pokemon(request):
    query = request.GET.get('q', '').lower()
    pokemon_list = Pokemon.objects.all()

    if query:
        pokemon_list = pokemon_list.filter(
            Q(name__icontains=query) |
            Q(alternate_names__icontains=[query])
        )

    return render(request, 'pokemon_list.html', {'pokemon_list': pokemon_list})


def pokemon_list(request):
    query = request.GET.get('q')  # Get search query
    pokemon_list = Pokemon.objects.all()

    if query:
        pokemon_list = pokemon_list.filter(
            Q(name__icontains=query) |  # Search by name
            Q(rank__icontains=query) |  # Search by rank
            Q(tier__icontains=query)    # Search by tier
        )

    return render(request, 'catalogue/pokemon_list.html', {'pokemon_list': pokemon_list, 'query': query})

#TODo Should change ranks to be ints
def pokemon_list_view(request):
    pokemon_list = sorted(Pokemon.objects.all(), key=lambda p: int(p.rank))
    synergies = Synergy.objects.all()  # Pass full objects, not just names
    context = {
        'pokemon_list': pokemon_list,
        'synergies': synergies,
    }
    return render(request, 'pokemon_list.html', context)


def item_list(request):
    query = request.GET.get("q", "")  # Get search query
    item_list = Item.objects.all()

    if query:
        item_list = item_list.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )

    return render(request, "catalogue/item_list.html", {"item_list": item_list, "query": query})


def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    recommended_pokemon = Pokemon.objects.filter(recommended_items=item)

    # Prepare the data for the recommended Pokémon
    recommended_pokemon_data = [
        {
            "name": pokemon.name,
            "slug": pokemon.slug,
            "image_url": pokemon.images.first().image.url if pokemon.images.exists() else ""
        }
        for pokemon in recommended_pokemon
    ]

    return JsonResponse({
        "name": item.name,
        "description": item.description,
        "image_url": item.picture.url if item.picture else "",
        "recommended_pokemon": recommended_pokemon_data
    })



def synergy_detail_json(request, slug):
    synergy = get_object_or_404(Synergy, slug=slug)
    associated_pokemon = synergy.pokemon.all()
    associated_pokemon_data = [
        {
            "name": pokemon.name,
            "slug": pokemon.slug,
            "image_url": pokemon.images.first().image.url if pokemon.images.exists() else ""
        }
        for pokemon in associated_pokemon
    ]
    return JsonResponse({
        "name": synergy.name,
        "description": synergy.descriptions,
        "image_url": synergy.picture.url if synergy.picture else "",
        "associated_pokemon": associated_pokemon_data
    })

def synergy_detail(request, slug):
    synergy = get_object_or_404(Synergy, slug=slug)
    return render(request, 'catalogue/synergy_detail.html', {'synergy': synergy})

def synergy_list(request):
    query = request.GET.get('q', '')  # Get search query
    synergy_list = Synergy.objects.all()

    if query:
        synergy_list = synergy_list.filter(
            Q(name__icontains=query) |  # Search by name
            Q(descriptions__icontains=query)  # Search by description
        )

    return render(request, 'catalogue/synergy_list.html', {'synergy_list': synergy_list, 'query': query})

def pokemon_detail(request, pokemon_slug):
    pokemon = get_object_or_404(Pokemon, slug=pokemon_slug)
    return render(request, 'catalogue/pokemon_detail.html', {'pokemon': pokemon})


def home(request):
    # Fetch some featured Pokémon, items, and synergies for the home page
    featured_pokemon = Pokemon.objects.all()[:3]  # Display the first 3 Pokémon
    featured_items = Item.objects.all()[:3]  # Display the first 3 items
    featured_synergies = Synergy.objects.all()[:3]  # Display the first 3 synergies

    context = {
        'featured_pokemon': featured_pokemon,
        'featured_items': featured_items,
        'featured_synergies': featured_synergies,
    }
    return render(request, 'catalogue/home.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('home')  # Redirect to a home or dashboard page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
