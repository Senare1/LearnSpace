# Generated by Django 5.0.6 on 2024-07-21 22:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(blank=True, max_length=32, null=True)),
                ('learner_phone', models.CharField(blank=True, max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Telephone')),
                ('learner_email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('learner_level', models.CharField(blank=True, choices=[('SIXIEME', 'SIXIEME'), ('CINQUIEME', 'CINQUIEME'), ('TROISIEME', 'TROISIEME'), ('QUATRIEME', 'QUATRIEME'), ('SECONDE', 'SECONDE'), ('PREMIERE', 'PREMIERE'), ('TERMINAL', 'TERMINAL')], max_length=128, null=True, verbose_name='Classe')),
                ('is_first_cycle', models.BooleanField(default=False)),
                ('teacher_register', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Matricule')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_learner', models.BooleanField(default=True)),
                ('learner_subscription', models.CharField(blank=True, choices=[('STANDARD', 'STANDARD'), ('PREMIUM', 'PREMIUM')], default='STANDARD', max_length=12, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
