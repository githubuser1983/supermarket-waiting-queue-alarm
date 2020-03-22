from django.urls import path
from django.contrib.auth import views as auth_views

# from . import views

app_name = "users"

urlpatterns = [
    path("users/login/", auth_views.LoginView.as_view(
            template_name="users/login.html",
            #authentication_form=LoginForm,
            #redirect_field_name='companies:select',
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("users/logout/", auth_views.LogoutView.as_view(
            template_name="users/logout.html",
            #redirect_field_name='users:login',
        ),
        name="logout",
    ),
]
