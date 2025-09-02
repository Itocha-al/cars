from django.contrib import admin
from django.contrib import messages
from .models import Profile, Comment, ModelSuggestion
from cars.models import CarModel, Brand


@admin.register(ModelSuggestion)
class ModelSuggestionAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_name', 'year', 'suggested_by', 'created_at', 'is_reviewed']
    list_filter = ['brand', 'is_reviewed', 'created_at', 'year']
    search_fields = ['model_name', 'description', 'suggested_by__username']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Информация о модели', {
            'fields': ('brand', 'model_name', 'year')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Пользователь и статус', {
            'fields': ('suggested_by', 'is_reviewed', 'created_at')
        }),
    )

    actions = ['mark_as_reviewed']

    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(is_reviewed=True)
        self.message_user(request, f'{updated} предложени{"е" if updated == 1 else "й"} отмечено как рассмотренное.')
    mark_as_reviewed.short_description = "Отметить как рассмотренные"

    # при сохранении — создать CarModel, если is_reviewed=True
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # если помечено как рассмотренное — создаём модель
        if obj.is_reviewed and not obj.notified:  # только если ещё не уведомляли
            car_model, created = CarModel.objects.get_or_create(
                brand=obj.brand,
                name=obj.model_name,
                defaults={
                    'year_released': obj.year or 1990,
                    'history': 'Добавлено из предложения пользователя.',
                    'why_cult': obj.description,
                    'value': 'Информация будет добавлена позже.',
                    'image': obj.image
                }
            )

            if not created and obj.image and not car_model.image:
                car_model.image = obj.image
                car_model.save()

            # отправляем уведомление автору
            try:
                from django.contrib.auth.models import User
                user = obj.suggested_by
                # добавляем сообщение в систему Django messages
                messages.success(
                    user,
                    f'Привет, {user.username}! '
                    f'Твоя предложенная модель "{obj.brand.name} {obj.model_name}" '
                    f'была добавлена в базу сайта! Спасибо за вклад 🚗✨'
                )
                # отмечаем, что уведомили
                obj.notified = True
                obj.save(update_fields=['notified'])
            except Exception as e:
                # на случай ошибки (например, отключены сообщения)
                pass

            messages.success(
                request,
                f'Модель "{obj.brand.name} {obj.model_name}" добавлена в базу!'
            )
