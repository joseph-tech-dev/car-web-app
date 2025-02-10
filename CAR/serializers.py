from rest_framework import serializers
from .models import (
    User, Car, CarImage, Wishlist, CarComparison, Review, Message, SearchHistory, Transaction
)
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterPostSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['password', 'username', 'last_name', 'first_name', 'email', 'phone', 'profile_image']

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id', 'dealer', 'make', 'model', 'year', 'price', 'mileage', 'condition', 'transmission', 'fuel_type', 'color', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'dealer', 'created_at', 'updated_at']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'car', 'image', 'image_type']
        read_only_fields = ['id']


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'car']
        read_only_fields = ['id', 'user']


class CarComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarComparison
        fields = ['id', 'user', 'car1', 'car2']
        read_only_fields = ['id', 'user']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'car', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'subject', 'message', 'created_at', 'read_at']
        read_only_fields = ['id', 'sender', 'created_at', 'read_at']


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'search_term', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'car', 'price', 'created_at']
        read_only_fields = ['id', 'buyer', 'created_at']
