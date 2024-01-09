from django.shortcuts import render, redirect
from django.views.generic import FormView
from accounts.forms import UserRegistrationForm, UserUpdateForm
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


# Create your views here.
def send_authentication_email(user, to_user, subject, template):
    message = render_to_string(
        template,
        {
            "user": user,
        },
    )
    to_email = to_user
    send_email = EmailMultiAlternatives(subject, "", to=[to_email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class UserRegistrationView(FormView):
    template_name = "accounts/user_registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("register")

    def form_valid(self, form):
        # print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)  # ei functionta nije nije call hocce


class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy("home")


class UserBankAccountUpdateView(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")  # Redirect to the user's profile page
        return render(request, self.template_name, {"form": form})


@login_required(login_url="/accounts/login/")
def change_pass(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            change_form = PasswordChangeForm(user=request.user, data=request.POST)
            if change_form.is_valid():
                change_form.save()
                messages.success(request, "Yor password changed successfully")
                send_authentication_email(
                    request.user,
                    request.user.email,
                    "Changed password successfully",
                    "accounts/success_pass_change.html",
                )
                update_session_auth_hash(request, change_form.user)
                return redirect("profile")
        else:
            change_form = PasswordChangeForm(user=request.user)
        return render(request, "accounts/change_pass.html", {"form": change_form})
    else:
        return redirect("login")
