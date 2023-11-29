from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from app.views import *

router = DefaultRouter()
router.register('', ProductView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', CreateUserAPIView.as_view(), name='signup'),    
    path('logout/', LogoutView.as_view(), name='logout' ),
    path('products/', include(router.urls)),
    path('', CustomTokenObtainPairView.as_view(), name='create'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='refresh'),
    path('verify/', CustomTokenVerifyView.as_view(), name='verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
