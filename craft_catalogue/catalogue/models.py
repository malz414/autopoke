from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Example custom field
    bio = models.TextField(blank=True)  # Example custom field
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Example custom field

    def __str__(self):
        return self.username


# class Artist(models.Model):
#     name = models.CharField(max_length=255)
#     bio = models.TextField(blank=True)
#     profile_picture = models.ImageField(upload_to='artists/', blank=True, null=True)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15, blank=True)
#     website = models.URLField(blank=True)
#     social_media_links = models.JSONField(blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True)
#     date_joined = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


from django.db import models
from django.utils.text import slugify

class Pokemon(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    attack = models.IntegerField(blank=True, default=0)
    defense = models.IntegerField(blank=True, default=0)
    special_attack = models.IntegerField(blank=True, default=0)
    special_defense = models.IntegerField(blank=True, default=0)
    attack_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    critical_hit_rate = models.IntegerField(help_text="Percentage value (e.g., 10 for 10%)", blank=True, default=0)
    critical_hit_damage_bonus_rate = models.IntegerField(help_text="Percentage value (e.g., 20 for 20%)", blank=True, default=0)

    rank = models.IntegerField(blank=True, null=True)
    tier = models.IntegerField(blank=True, null=True)

    stats_per_level = models.JSONField(blank=True, null=True)

    ability_1_name = models.CharField(max_length=255, blank=True)
    ability_1_description = models.TextField(blank=True)
    ability_1_picture = models.ImageField(upload_to='ability_pictures/', blank=True, null=True)  # New field for ability 1 picture

    ability_2_name = models.CharField(max_length=255, blank=True)
    ability_2_description = models.TextField(blank=True)
    ability_2_picture = models.ImageField(upload_to='ability_pictures/', blank=True, null=True)  # New field for ability 2 picture

    unite_move_name = models.CharField(max_length=255, blank=True)
    unite_move_description = models.TextField(blank=True)
    unite_move_activation = models.TextField(blank=True, default="")
    unite_move_picture = models.ImageField(upload_to='move_pictures/', blank=True, null=True)

    recommended_items = models.ManyToManyField('Item', blank=True)
    recommended_number = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'),  (3, '3')], default=1)

    alternate_names = models.TextField(blank=True, default="")

    hp = models.IntegerField(blank=True, null=True)
    mp = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class LevelStats(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='level_stats')
    level = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    special_attack = models.IntegerField()
    special_defense = models.IntegerField()
    attack_speed = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Level {self.level} stats for {self.pokemon.name}"
    
class PokemonImage(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pokemon_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.pokemon.name}"
    
from django.utils.text import slugify

class Item(models.Model):
    picture = models.ImageField(upload_to='items/')
    name = models.CharField(max_length=255, unique=True) 
    description = models.TextField()
    synergistic_pokemon = models.ManyToManyField('Pokemon', blank=True, related_name='synergistic_items')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Synergy(models.Model):
    picture = models.ImageField(upload_to='synergies/')
    name = models.CharField(max_length=255, unique=True) 
    pokemon = models.ManyToManyField('Pokemon', blank=True, related_name='synergies')
    descriptions = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
# class CartItem(models.Model):
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
#     item = models.ForeignKey(CraftItem, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     @property
#     def total_price(self):
#         return self.quantity * self.item.price

# class Cart(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey('catalogue.CustomUser', null=True, blank=True, on_delete=models.SET_NULL)
    
#     def total_price(self):
#         return sum(cart_item.total_price for cart_item in self.cart_items.all())

#     def __str__(self):
#         return f"Cart {self.id} for {self.user.username if self.user else 'Guest'}"