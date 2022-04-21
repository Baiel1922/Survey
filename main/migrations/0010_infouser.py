# Generated by Django 3.2.7 on 2022-04-21 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0009_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='media/user_image')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='info_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Info_student',
                'verbose_name_plural': 'Info_studets',
            },
        ),
    ]