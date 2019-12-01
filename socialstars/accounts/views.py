from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render

from accounts.forms import UserForm, UserProfileInfoForm, EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from social.models import Friend


def index(request):
    return render(request, 'accounts/index.html')


def register(request):
    """
    This view function is used to Register new users to
    website, using UserForm and UserProfileInfoForm from
    forms.py . verify all data and save it in User and UserProfileInfo
    Tables
    :param request:
    :return:
    """
    # to send template to check user authorization
    registered = False

    if request.method == "POST":
        # get all data post in form through request and save it in user_form , profile_form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # check if post data is valid
        if user_form.is_valid() and profile_form.is_valid():

            # if valid save data in User and UserProfileInfo tables in Database
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.bio = request.POST.get('bio')
            profile.birth_date = request.POST.get('birth_date')

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'accounts/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered
                   })


def user_login(request):
    """
    This view function is used to Login registered users to
    website, using Login form. verify login details from database
    using django.admin builtin function authenticate
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user from Database
        user = authenticate(username=username, password=password)

        # if user is authenticated
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('social:home'))
            else:
                return HttpResponse("Account is Inactive")

        else:
            return HttpResponse("Invalid login details")

    else:
        return render(request, 'accounts/index.html', {})


@login_required()
def user_logout(request):
    """
    Logout authenticated users from website
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect(reverse('accounts:index'))


@login_required()
def user_profile(request, pk=None):
    """
    Provide user profile page consisting of all
    current users details
    :param request:
    :return:
    """

    if pk:
        current_user = User.objects.get(pk=pk)
    else:
        current_user = request.user

    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        if current_user in friends:
            is_friend = True
        else:
            is_friend = False

    except Friend.DoesNotExist:
        friends = None
        friend = None
        is_friend = False

    args = {'user': current_user, 'is_friend': is_friend, 'friend': friend, 'pk': pk}
    return render(request, 'accounts/profile.html', args)


@login_required()
def edit_profile(request):
    """"
    Edit current user profile, get instance of request user
    goto EditProfileForm inherit from ChangeForm
    """
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts:profile'))

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required()
def change_password(request):
    """
    Change Login user password using
    Builtin class PasswordChangeForm from Django.contrib.auth.forms
    :param request:
    :return:
    """
    if request.method == "POST":

        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            return HttpResponseRedirect(reverse('accounts:change-password.html'))

    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/edit_profile.html', {'form': form})
