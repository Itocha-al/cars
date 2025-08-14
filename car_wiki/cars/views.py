from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm
from django.shortcuts import get_object_or_404
from .models import Brand, CarModel


def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'cars/brands.html', {'brands': brands})


def model_list(request, brand_id):
    brand = get_object_or_404(Brand, id=brand_id)
    models = brand.models.all()
    return render(request, 'cars/models.html', {'brand': brand, 'models': models})


def model_detail(request, model_id):
    car_model = get_object_or_404(CarModel, id=model_id)
    return render(request, 'cars/model_detail.html', {'model': car_model})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему!')
            return redirect('brand_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = SignUpForm()
    return render(request, 'cars/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('brand_list')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AuthenticationForm()
    return render(request, 'cars/login.html', {'form': form})


def user_logout(request):
    username = request.user.username
    from django.contrib.auth import logout
    logout(request)
    messages.info(request, f'Вы успешно вышли из аккаунта {username}.')
    return redirect('brand_list')
