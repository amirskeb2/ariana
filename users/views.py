from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from users.forms import RegistrationForm, MyUserAuthenticationForm, AccountUpdateForm


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            phone_number = form.cleaned_data.get('phone_number')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(phone_number=phone_number, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form
    else:  # for GET request
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = MyUserAuthenticationForm(request.POST)
        if form.is_valid():
            phone_number = request.POST['phone_number']
            password = request.POST['password']
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = MyUserAuthenticationForm()

    context['login_form'] = form
    return render(request, 'users/login.html', context)


def account_view(request):

    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            initial = {
                'profile_pic': request.POST['profile_pic'],
                'phone_number': request.POST['phone_number'],
                'email': request.POST['email'],
                'username': request.POST['username'],
                'first_name': request.POST['first_name'],
                'last_name': request.POST['last_name'],
            }
            form.save()
            context['success_message'] = 'اطلاعات حساب شما بروزرسانی شد'
    else:
        form = AccountUpdateForm(
            initial={
                'profile_pic': request.user.profile_pic,
                'phone_number': request.user.phone_number,
                'email': request.user.email,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        )
    context['account_form'] = form
    return render(request, 'users/account.html', context)


def must_authenticate_view(request):
    return render(request, 'users/must_authenticate.html', {})
