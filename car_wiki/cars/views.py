from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Brand, CarModel
from accounts.forms import CommentForm, ModelSuggestionForm
from accounts.models import Comment, ModelSuggestion


class BrandListView(ListView):
    model = Brand
    template_name = 'cars/brands.html'
    context_object_name = 'brands'
    queryset = Brand.objects.all()


class ModelListView(DetailView):
    model = Brand
    template_name = 'cars/models.html'
    context_object_name = 'brand'
    pk_url_kwarg = 'brand_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['models'] = self.object.models.all()

        # Форма предложения
        if self.request.user.is_authenticated:
            context['suggestion_form'] = ModelSuggestionForm(
                initial={'brand': self.object}
            )
        else:
            context['suggestion_form'] = None

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы предложить модель, войдите в аккаунт.')
            return redirect('login')

        form = ModelSuggestionForm(request.POST, request.FILES)
        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.suggested_by = request.user
            suggestion.save()
            messages.success(request, 'Спасибо! Ваша модель отправлена на рассмотрение.')
        else:
            messages.error(request, 'Проверьте данные формы.')
        return redirect('model_list', brand_id=kwargs['brand_id'])


class CarModelDetailView(DetailView):
    model = CarModel
    template_name = 'cars/model_detail.html'
    context_object_name = 'model'
    pk_url_kwarg = 'model_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Чтобы оставить комментарий, войдите в аккаунт.')
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car_model = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
        else:
            messages.error(request, 'Проверьте текст комментария.')
        return redirect('model_detail', model_id=self.object.id)


# --- Остальные классы: SignUpView, LoginView, LogoutView ---
class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'cars/signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались и вошли в систему!')
            return redirect('brand_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
        return render(request, 'cars/signup.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'cars/login.html', {'form': form})

    def post(self, request):
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
        return render(request, 'cars/login.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        username = request.user.username
        logout(request)
        messages.info(request, f'Вы успешно вышли из аккаунта {username}.')
        return redirect('brand_list')
