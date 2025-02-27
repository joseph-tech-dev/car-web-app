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
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import EmailMessage
from .utils import generate_payment_receipt
from django.contrib.auth import logout
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils import timezone
from .authentication import CustomJWTAuthentication


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
                key=settings.SIMPLE_JWT["AUTH_COOKIE_NAME"],
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

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Force authentication manually
        user, token = CustomJWTAuthentication().authenticate(request)
        
        if user is None:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            logout(request)

            refresh_token = request.COOKIES.get("refresh_token")
            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()
                except TokenError:
                    return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

            response = Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)
            response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE_NAME"], samesite="Lax", secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"])
            response.delete_cookie("refresh_token", samesite="Lax", secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"])
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CarListCreateAPIView(APIView):
    permission_classes = [IsSuperuserOrReadOnly]
    
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
    
    def delete(self, request, pk):
        wishlist = get_object_or_404(Wishlist, pk=pk)
        wishlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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

class InitiatePaymentAPIView(APIView):
    #permission_classes = [IsAuthenticated]

    def post(self, request):
        """Initiates a PayPal transaction and returns the PayPal URL."""
        car_id = request.data.get('car_id')
        car = get_object_or_404(Car, car_id=car_id)
        r = request.data.get('id')
        user = User.objects.get(id=r)
        transaction = Transaction.objects.create(
            #buyer=request.user,
            buyer=user,
            car=car,
            amount=car.price,
            status="pending"
        )

        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": str(transaction.amount),
            "item_name": f"Purchase of {car.make} {car.model}",
            "invoice": str(transaction.transaction_id),
            "currency_code": "USD",
            "notify_url": f"{request.scheme}://{request.get_host()}/scs/paypal/ipn/",
            "return_url": f"{request.scheme}://{request.get_host()}/scs/paypal/success/?transaction_id={transaction.transaction_id}",
            "cancel_return": f"{request.scheme}://{request.get_host()}/scs/paypal/failure/?transaction_id={transaction.transaction_id}",
        }

        form = PayPalPaymentsForm(initial=paypal_dict)
        return Response({"paypal_url": form.get_html()}, status=status.HTTP_200_OK)


class PaymentSuccessAPIView(APIView):
    """Handles successful PayPal payment"""
    def get(self, request):
        transaction_id = request.GET.get("transaction_id")
        transaction = get_object_or_404(Transaction, id=transaction_id)

        transaction.status = "completed"
        transaction.save()

        # Generate and send PDF receipt
        pdf_buffer = generate_payment_receipt(transaction)
        pdf_filename = f"Receipt_{transaction.transaction_id}.pdf"

        # Send receipt via email
        self.send_pdf_receipt(transaction, pdf_buffer, pdf_filename)
        return Response({"message": "Payment successful", "transaction_id": transaction.id}, status=status.HTTP_200_OK)

    def send_pdf_receipt(self, transaction, pdf_buffer, pdf_filename):
        # Email generated PDF receipt to the buyer

        email = EmailMessage(
            subject="Payment Receipt",
            body = f"Hello {transaction.buyer.username},\n\n"
                  f"Attached is your payment receipt for the car purchase"
                 f"Thank you for choosing HotWheelIQ Car Dealership",
            from_email="noreply@hotwheel.com",
            to = [transaction.buyer.email],

        )
        email.attach(pdf_filename, pdf_buffer, 'application/pdf')
        # Send Email
        email.send()
        


class PaymentFailureAPIView(APIView):
    """Handles failed PayPal payment"""
    def get(self, request):
        transaction_id = request.GET.get("transaction_id")
        transaction = get_object_or_404(Transaction, id=transaction_id)
        
        transaction.status = "failed"
        transaction.save()

        return Response({"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)




from django.core.mail import send_mail
from django.conf import settings
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            # Prepare email content
            email_message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
            
            send_mail(
                subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Change this if you want to send to different email addresses
                fail_silently=False,
            )
            
            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ReviewList(APIView):
    #permission_classes = [AllowAny]  # Adjust based on your authorization needs

    def get(self, request, product_id=None):
        if product_id:
            reviews = Review.objects.filter(product_id=product_id)
        else:
            reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Set the 'user' field to the logged-in user
        if request.user.is_authenticated:
            serializer = ReviewSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Automatically set the user field
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Authentication required'}, status=status.HTTP_403_FORBIDDEN)

class ReviewDetail(APIView):
    #permission_classes = [AllowAny]  # Adjust based on your authorization needs

    def get_object(self, review_id):
        try:
            return Review.objects.get(pk=review_id)
        except Review.DoesNotExist:
            return None

    def get(self, request, review_id):
        review = self.get_object(review_id)
        if review:
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, review_id):
        review = self.get_object(review_id)
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        # Add permission check here if needed
        if request.user != review.user:  # Optionally restrict editing to the review's author
            return Response({"error": "You do not have permission to update this review"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, review_id):
        review = self.get_object(review_id)
        if not review:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        # Add permission check here if needed
        if request.user != review.user:  # Optionally restrict deletion to the review's author
            return Response({"error": "You do not have permission to delete this review"}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


