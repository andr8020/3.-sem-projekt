# users/views.py

from django.views.generic import CreateView, DetailView

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from photoapp.models import Profile
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EditProfileForm


class SignUpView(CreateView):

    template_name = 'users/signup.html'

    form_class = UserCreationForm

    success_url = reverse_lazy('photo:list')

    def form_valid(self, form):
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )

        login(self.request, user)

        return to_return


class CustomLoginView(LoginView):

    template_name = 'users/login.html'


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'users/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        #users = Profile.objects.all()
        context = super(ShowProfilePageView,
                        self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])

        context["page_user"] = page_user
        return context


def logout_user(request):
    logout(request)
    return redirect('list')


class UserEditView(DetailView):
    form_class = EditProfileForm
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('list')

    def get_object(self):
        return self.request.user
