from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User,Car, CarImage, Wishlist, CarComparison, Review, Message, SearchHistory, Transaction
from .serializers import (
    CarSerializer,
    CarImageSerializer,
    WishlistSerializer,
    ReviewSerializer,
    MessageSerializer,
    SearchHistorySerializer,
    RegisterPostSerializer,
    TransactionSerializer,
    CarComparisonSerializer
)
from .authentication import get_tokens_for_user
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .permissions import IsSuperuserOrReadOnly

User = get_user_model()

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = RegisterPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)

            response = Response({"message": "Login successful!"})
            response.set_cookie(
                key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                value=tokens["access"],
                httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
            )
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                samesite="Lax",
            )
            return response

        return Response({"error": "Invalid credentials"}, status=401)
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logout successful!"})
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        response.delete_cookie("refresh_token")
        return response

class CarListCreateAPIView(APIView):
    #permission_classes = [IsSuperuserOrReadOnly]
    
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dealer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarDetailAPIView(APIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarSerializer(car, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CarImageAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        images = CarImage.objects.all()
        serializer = CarImageSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CarImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WishlistAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        wishlist = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarComparisonAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = CarComparisonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        """Send a new message"""
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(sender=request.user)  # Sender is always the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        "Send a message to another user"
        serializer = MessageSerializer(data=request.data)
        
        # To be removed
        user = request.data.get('sender')
        sender = User.objects.get(id=user)

        if serializer.is_valid():
            #serializer.save(sender=request.user)
            serializer.save(sender=sender)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatHistoryAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def get(self, request, receiver_id):
        """Retrieve messages between authenticated user and a specific receiver"""
        sender = request.user
        messages = Message.objects.filter(
            Q(sender=sender, receiver_id=receiver_id) | 
            Q(sender_id=receiver_id, receiver=sender)
        ).order_by("timestamp")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchHistoryAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        search_history = SearchHistory.objects.filter(user=request.user)
        serializer = SearchHistorySerializer(search_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = SearchHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarRecommendationAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # AI/ML logic to recommend cars based on search history
        recommended_cars = []  # Placeholder for ML-generated recommendations
        return Response(recommended_cars, status=status.HTTP_200_OK)

class TransactionAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(buyer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

