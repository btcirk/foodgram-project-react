# Generated by Django 4.1 on 2022-08-30 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipies', '0004_alter_recipe_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='measurement_unit',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='name',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='amount',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=4, verbose_name='Количество'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='recipies.food', verbose_name='Ингредиент'),
            preserve_default=False,
        ),
    ]
