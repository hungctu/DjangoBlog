# Generated by Django 4.2 on 2023-04-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_alter_book_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='date_create',
            field=models.DateField(auto_now=True),
        ),
    ]
