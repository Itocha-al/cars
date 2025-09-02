from django.db import models
from django.contrib.auth.models import User
from cars.models import Brand, CarModel
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- Профиль пользователя ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"


# --- Комментарии к моделям автомобилей ---
class Comment(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} → {self.car_model.name}'

    class Meta:
        ordering = ['-created_at']  # новые комментарии сверху


# --- Предложение новой модели автомобиля ---
class ModelSuggestion(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Марка")
    model_name = models.CharField("Название модели", max_length=100)
    year = models.PositiveIntegerField("Год выпуска", blank=True, null=True)
    description = models.TextField("Описание", help_text="Почему эта модель культовая?")
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Предложил")
    image = models.ImageField(
        "Фото автомобиля",
        upload_to='suggested_cars/',
        blank=True,
        null=True,
        help_text="Загрузите фото автомобиля (по желанию)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField("Рассмотрено", default=False)

    def __str__(self):
        return f"{self.brand.name} {self.model_name} (от {self.suggested_by.username})"
    notified = models.BooleanField("Уведомлен", default=False)

    class Meta:
        verbose_name = "Предложение модели"
        verbose_name_plural = "Предложения моделей"
        ordering = ['-created_at']


# --- сигналы для автоматического создания профиля ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
