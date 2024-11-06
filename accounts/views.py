from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from .models import User

# Factory pattern for user views
class UserFactory:
    @staticmethod
    def create_user_view(view_type):
        if view_type == "register":
            return RegisterView.as_view()
        elif view_type == "login":
            return LoginView.as_view()
        else:
            raise ValueError("Invalid view type")

# Registration View
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "../templates/register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("home")
        return render(request, "../templates/register.html", {"form": form})

# Login View
class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "../templates/login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        return render(request, "../templates/login.html", {"form": form})


# Create your views here.
