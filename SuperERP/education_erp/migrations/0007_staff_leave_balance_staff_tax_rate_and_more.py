# Generated by Django 4.2.20 on 2025-03-17 20:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('education_erp', '0006_timetable_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='leave_balance',
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name='staff',
            name='tax_rate',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='educationuser',
            name='erp_role',
            field=models.CharField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('staff', 'Staff')], default='staff', max_length=50),
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('grade_value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_recorded', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grades', to='education_erp.student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('present', models.BooleanField(default=False)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='education_erp.student')),
            ],
        ),
    ]
