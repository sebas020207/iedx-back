from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import UserView, AllUsersView, UserImages, CreateUserView, MyInfoView, ChangePasswordView, UserCountView

urlpatterns = [
    path('user', CreateUserView.as_view()),
    path('my_info', MyInfoView.as_view()),
    path('user/<int:pk>', UserView.as_view()),
    path('users', AllUsersView.as_view()),
    path('users/count', UserCountView.as_view()),
    path('user/images/<int:pk>', UserImages.as_view()),
    path('user/password', ChangePasswordView.as_view()),
    path('login', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),

    # path('login', LoginView.as_view()),
    # path('user', UserView.as_view()),
    # path('logout', LogoutView.as_view()),
]
