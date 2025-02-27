from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

# User Model (Extending Django's default User)
class User(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('dealer', 'Dealer'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="car_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="car_user_permissions", blank=True)

    def __str__(self):
        return self.username

# Car Model
class Car(models.Model):
    car_id = models.CharField(primary_key=True, max_length=7, editable=False)
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]

    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]
    color = models.CharField(max_length=20)
    dealer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    transmission = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=(models.DateTimeField(auto_now=True))

    def save(self, *args, **kwargs):
        if not self.car_id:
            self.car_id = f"CID-{str(uuid.uuid4()).upper()[:7]}"
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"

# Car Images Model (Stores multiple images per car)
class CarImage(models.Model):
    IMAGE_TYPES = [
        ('front', 'Front View'),
        ('side', 'Side View'),
        ('back', 'Back View'),
        ('interior', 'Interior View'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="car_images/")
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES)

    def __str__(self):
        return f"{self.car.make} {self.car.model} - {self.image_type}"

# Wishlist Model
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')

    def __str__(self):
        return f"{self.user.username} - {self.car.make} {self.car.model}"

# Car Comparison Model
class CarComparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car1 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comparison_car1')
    car2 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comparison_car2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} compared {self.car1.make} {self.car1.model} & {self.car2.make} {self.car2.model}"

# Reviews & Ratings
# reviews/models.py
from django.conf import settings

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to your custom User model
    review = models.TextField()
    rating = models.PositiveIntegerField()  # Rating should be a positive integer
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review for Product {self.id} by {self.user.username}'
# Messaging System (Buyer to Dealer)
class Message(models.Model):
    message_id = models.CharField(primary_key=True, max_length=7, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=True, null=True)  # Optional: Message related to a car
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.message_id:
            self.message_id = f'MSG-{str(uuid.uuid4()).upper()[:7]}'
        return super().save(*args,**kwargs)
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

# User search history
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    search_query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} searched '{self.search_query}'"

# Transactions (Purchase History)
class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=7, editable=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"TS-{str(uuid.uuid4()).upper()[:7]}"
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.buyer.username} - {self.amount}"
# Advertisement & Featured Listings
class Advertisement(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="advertisements")
    dealer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_featured = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Ad for {self.car.make} {self.car.model} by {self.dealer.username}"



