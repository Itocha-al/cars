from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cars', '0001_initial'),  # указать последнюю миграцию
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=254, verbose_name='email address'),
        ),
    ]
