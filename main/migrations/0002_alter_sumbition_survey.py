# Generated by Django 3.2.7 on 2022-02-19 02:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sumbition',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sumbitions', to='main.survey'),
        ),
    ]