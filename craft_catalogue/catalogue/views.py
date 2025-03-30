from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .forms import CustomAuthenticationForm  # If using the custom form
from .models import Pokemon, Item, Synergy
from django.db.models import Q  # For filtering
from django.http import JsonResponse
from django.http import HttpResponse

def search_pokemon(request):
    query = request.GET.get('q', '').lower()
    pokemon_list = Pokemon.objects.all()

    if query:
        pokemon_list = pokemon_list.filter(
            Q(name__icontains=query) |
            Q(alternate_names__icontains=[query])
        )

    return render(request, 'pokemon_list.html', {'pokemon_list': pokemon_list})


def filter_pokemon(queryset, query):
    """Filter Pokémon by name, rank, and tier."""
    if query:
        return queryset.filter(
            Q(name__icontains=query) |  
            Q(rank__icontains=query) |  
            Q(tier__icontains=query)   
        )
    return queryset

def pokemon_list(request):
    query = request.GET.get('q', '')  
    pokemon_list = filter_pokemon(Pokemon.objects.all(), query)
    synergies = Synergy.objects.all()

    return render(request, 'catalogue/pokemon_list.html', {
        'pokemon_list': pokemon_list,
        'query': query,
        'synergies': synergies
    })




def team_builder(request):
    query = request.GET.get('q', '')  
    rank_filter = request.GET.get('rank', '')  
    synergy_filter = request.GET.get('synergy', '')  

    # Start with all Pokémon and synergies
    pokemon_list = filter_pokemon(Pokemon.objects.all(), query)
    synergy_list = Synergy.objects.all()

    # Apply additional filters
    if rank_filter:
        pokemon_list = pokemon_list.filter(rank=rank_filter)

    if synergy_filter:
        pokemon_list = pokemon_list.filter(synergies__name__icontains=synergy_filter)

    return render(request, 'catalogue/team_builder.html', {
        'pokemon_list': pokemon_list,
        'synergy_list': synergy_list,
        'query': query,
        'rank_filter': rank_filter,
        'synergy_filter': synergy_filter
    })
def ads_txt(request):
    content = "google.com, pub-3195983389027090, DIRECT, f08c47fec0942fa0"
    return HttpResponse(content, content_type="text/plain")

#TODo Should change ranks to be ints
def pokemon_list_view(request):
    pokemon_list = sorted(Pokemon.objects.all(), key=lambda p: int(p.rank))

    return render(request, 'pokemon_list.html', {'pokemon_list': pokemon_list})

def patch_notes(request):
    pokemon_list = Pokemon.objects.all()  # Retrieve all Pokémon objects
    context = {"pokemon_list": pokemon_list}
    return render(request,'catalogue/patch_notes.html', context) 

def mechanics(request):
    return render(request,'catalogue/mechanics.html') 



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
    
    # Separate recommendations by type
    regular_recommendations = Pokemon.objects.filter(recommended_items=item)
    sheep_recommendations = Pokemon.objects.filter(recommended_itemsSheep=item)
    sheep_bold_recommendations = Pokemon.objects.filter(recommended_itemsSheepBold=item)

    # Helper function to build data
    def build_data(queryset):
        return [
            {
                "name": pokemon.name,
                "slug": pokemon.slug,
                "image_url": pokemon.images.first().image.url if pokemon.images.exists() else ""
            }
            for pokemon in queryset
        ]

    return JsonResponse({
    "name": item.name,
    "description": item.description,
    "image_url": item.picture.url if item.picture else "",
    "recommended_pokemon": (
        list(build_data(regular_recommendations)) +
        list(build_data(sheep_recommendations)) +
        list(build_data(sheep_bold_recommendations))
    ),
    "regular_recommendations": build_data(regular_recommendations),
    "sheep_recommendations": build_data(sheep_recommendations),
    "sheep_bold_recommendations": build_data(sheep_bold_recommendations)
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

def installation(request):
    context = {
        'title': 'Installation Guide',
        'steps': [
            'Step 1: Download the software.',
            'Step 2: Run the installer.',
            'Step 3: Follow the on-screen instructions.',
        ]
    }
    return render(request, 'catalogue/installation.html', context)

def tier_list(request):
    tiers = [("Amazing", 1), ("Good", 2), ("Ok", 3), ("Weak", 4)] 
    pokemon_list = Pokemon.objects.all()  
    context = {"tiers": tiers, "pokemon_list": pokemon_list}
    return render(request, "catalogue/tier_list.html", context)





def synergy_list(request):
    query = request.GET.get('q', '') 
    synergy_list = Synergy.objects.all()
    print("Synergies:", list(synergy_list)) 

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
    featured_pokemon = Pokemon.objects.all()  # Display the first 3 Pokémon
    featured_items = Item.objects.all() # Display the first 3 items
    featured_synergies = Synergy.objects.all() # Display the first 3 synergies

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
