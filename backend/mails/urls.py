from django.urls import path
from rest_framework_simplejwt import views as jwt_views

#curl --header "Content-Type: application/json" -X POST http://0.0.0.0:8000/userapi/token/obtain/ --data '{"email":"test@test.com","password":"test123"}'
from rest_framework.routers import SimpleRouter
from .views import LoginViewSet, RegistrationViewSet, RefreshViewSet, SyncViewset, SendViewset


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'login', LoginViewSet, basename='login')
routes.register(r'register', RegistrationViewSet, basename='register')
routes.register(r'refresh', RefreshViewSet, basename='refresh')
# mail sync, send n retrieve
routes.register(r'sync', SyncViewset, basename='sync')
routes.register(r'send_mail', SendViewset, basename='send')




urlpatterns = [
    *routes.urls
]