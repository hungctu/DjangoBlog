# Generated by Django 4.2 on 2023-04-17 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
