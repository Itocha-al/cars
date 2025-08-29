from django.db import models
from django.contrib.auth.models import User
from cars.models import CarModel
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- профиль пользователя ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"


# --- комментарии к моделям автомобилей ---
class Comment(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} → {self.car_model.name}'

    class Meta:
        ordering = ['-created_at']  # новые комментарии сверху


# --- сигналы для автоматического создания профиля ---
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
