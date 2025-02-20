from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import(
    CarListCreateAPIView,
    CarDetailAPIView,
    CarImageAPIView,
    WishlistAPIView,
    CarComparisonAPIView,
    ReviewAPIView,
    MessageAPIView,
    SearchHistoryAPIView,
    TransactionAPIView,
    RegisterUserAPIView,
    LoginView,
    LogoutView,
    ChatHistoryAPIView
    )

urlpatterns = [
    path('scs/register/', RegisterUserAPIView.as_view(), name='register'),
    path('scs/login/', LoginView.as_view(), name='login'),
    path('scs/logout/', LogoutView.as_view(), name='logout'),
    path('scs/cars/', CarListCreateAPIView.as_view(), name='car-list-create'),
    path('scs/cars/<int:pk>/',CarDetailAPIView.as_view(), name='car-detail'),
    path('scs/car-images/',CarImageAPIView.as_view(), name='car-image'),
    path('scs/wishlist/',WishlistAPIView.as_view(), name='wishlist'),
    path('scs/car-comparison/',CarComparisonAPIView.as_view(), name='car-comparison'),
    path('scs/reviews/', ReviewAPIView.as_view(), name='reviews'),
    path('scs/messages/', MessageAPIView.as_view(), name='messages'),
    path('scs/search-history/',SearchHistoryAPIView.as_view(), name='search-history'),
    path('scs/transactions/',TransactionAPIView.as_view(), name='transactions'),
    path('scs/chat-history/',ChatHistoryAPIView.as_view(), name='chat-history'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)