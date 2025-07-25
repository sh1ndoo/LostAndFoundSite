# Generated by Django 5.2.3 on 2025-07-06 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumberOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='socials',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='vk',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
