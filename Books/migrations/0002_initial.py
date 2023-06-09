# Generated by Django 4.2 on 2023-04-17 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.chapter'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chapter',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.book'),
        ),
        migrations.AddField(
            model_name='category_book',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.book'),
        ),
        migrations.AddField(
            model_name='category_book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Books.category'),
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
