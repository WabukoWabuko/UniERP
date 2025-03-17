# Generated by Django 4.2.20 on 2025-03-17 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education_erp', '0002_alter_educationuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='educationuser',
            name='user',
        ),
        migrations.AddField(
            model_name='educationuser',
            name='email',
            field=models.EmailField(default='basilwabbs@gmail.com', max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='educationuser',
            name='password',
            field=models.CharField(default='education@gmail.com', max_length=128),
            preserve_default=False,
        ),
    ]
