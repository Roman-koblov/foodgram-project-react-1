# Generated by Django 4.0.6 on 2022-07-18 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0003_favorites_favorites_unique_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рецепт в корзине',
                'verbose_name_plural': 'Рецепты в корзине',
            },
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_cart'),
        ),
    ]
