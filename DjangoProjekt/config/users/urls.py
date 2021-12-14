# users/urls.py
from django.urls import path

from django.contrib.auth.views import LogoutView

from .views import ShowProfilePageView, SignUpView, CustomLoginView, UserEditView

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(),
         name='show_profile_page'),
    path('<int:pk>/edit_user/', UserEditView.as_view(), name='edit_user'),
]
