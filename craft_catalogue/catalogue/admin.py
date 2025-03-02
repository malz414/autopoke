from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Item, Synergy, Pokemon, PokemonImage

# Inline model for displaying multiple images
class PokemonImageInline(admin.TabularInline):  
    model = PokemonImage
    extra = 3  # Allows adding 3 new images at once (change as needed)

class PokemonAdmin(admin.ModelAdmin):
    inlines = [PokemonImageInline]  # Include inline images
    list_display = ('name', 'rank', 'tier')
    filter_horizontal = ('recommended_items',)

    fieldsets = (
        (None, {
            'fields': ('name', 'alternate_names', 'attack', 'defense', 'special_attack', 'special_defense', 'attack_speed', 'critical_hit_rate', 'critical_hit_damage_bonus_rate', 'rank', 'tier', 'stats_per_level')
        }),
        ('Abilities', {
            'fields': ('ability_1_name', 'ability_1_description', 'ability_1_picture', 'ability_2_name', 'ability_2_description', 'ability_2_picture'),
        }),
        ('Unite Move', {
            'fields': ('unite_move_name', 'unite_move_description', 'unite_move_activation', 'unite_move_picture'),
        }),
        ('Recommended Items', {
            'fields': ('recommended_items', 'recommended_number'),
        }),
        ('HP/MP', {
            'fields': ('hp', 'mp'),
        }),
    )

class SynergyAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriptions')
    filter_horizontal = ('pokemon',)  # Makes selecting Pokémon easier
    

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    filter_horizontal = ('synergistic_pokemon',)  # Makes selecting Pokémon easier
# Registering models with customizations
admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Synergy)
admin.site.register(Item)
