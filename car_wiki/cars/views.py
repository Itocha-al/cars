from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from .models import Brand, CarModel
from accounts.models import Comment
from accounts.forms import CommentForm


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
        return context


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
