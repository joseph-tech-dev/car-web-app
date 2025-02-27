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
        fields = ['car_id', 'dealer', 'make', 'model', 'year', 'price', 'mileage', 'condition', 'transmission', 'fuel_type', 'color', 'description', 'created_at', 'updated_at']
        read_only_fields = ['car_id', 'dealer', 'created_at', 'updated_at']


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['id', 'car_id', 'image', 'image_type']
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
        fields = ['message_id', 'sender', 'receiver','content', 'timestamp']
        read_only_fields = ['message_id', 'created_at', 'read_at']


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ['id', 'user', 'search_term', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'buyer', 'car', 'price', 'created_at']
        read_only_fields = ['transaction_id', 'buyer', 'created_at']


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=100)
    message = serializers.CharField()


# Review serializer
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username as a string instead of user ID
    class Meta:
        model = Review
        fields = ['id', 'user','review', 'rating','created_at', 'updated_at']
        read_only_fields = ['user']  # Prevent user from submitting their user ID in POST requests

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value