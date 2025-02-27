from django.contrib import admin
from .models import (User, 
                     Car, 
                     CarImage, 
                     Wishlist, 
                     CarComparison, 
                     Review, 
                     Message, 
                     SearchHistory, 
                     Transaction)

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_title = _("HotwheelsHQ")
admin.site.site_header = _("HotwheelsHQ")




class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('id','username', 'first_name','last_name','role', 'phone','email', 'profile_image')
admin.site.register(User, UserAdmin)

class CarAdmin(admin.ModelAdmin):
    model = Car
    list_display = ('car_id', 'make', 'model', 'year', 'color', 'price', 'mileage', 'fuel_type', 'transmission', 'condition')
admin.site.register(Car,CarAdmin)

class CarImageAdmin(admin.ModelAdmin):
    model = CarImage
    list_display = ('car', 'image', 'image_type')
admin.site.register(CarImage,CarImageAdmin)

class WishlistAdmin(admin.ModelAdmin):
    model = Wishlist
    list_display = ('user', 'car')
admin.site.register(Wishlist, WishlistAdmin)

class CarComparisonAdmin(admin.ModelAdmin):
    model = CarComparison
    list_display = ('user', 'car1', 'car2')
admin.site.register(CarComparison, CarComparisonAdmin)

class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('id','user','rating','review','created_at','updated_at')
admin.site.register(Review, ReviewAdmin)

class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('sender', 'receiver', 'car', 'content', 'timestamp')
admin.site.register(Message, MessageAdmin)

class SearchHistoryAdmin(admin.ModelAdmin):
    model = SearchHistory 
    list_display = ('user', 'search_query','created_at')
admin.site.register(SearchHistory, SearchHistoryAdmin)

class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ('buyer', 'car','amount','status')
admin.site.register(Transaction,TransactionAdmin)