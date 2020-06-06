# Generated by Django 2.2.5 on 2019-12-09 18:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LikeMeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=90, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('sex', models.IntegerField(default=0)),
                ('birth_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone_number', models.TextField(default=0)),
                ('photo', models.ImageField(default='profiles/profile_default.png', upload_to='profiles/')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='join date')),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('posteig_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='likeme.Comments')),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Posteig',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.CharField(max_length=200)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='likeme.Posteig')),
                ('user_like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('accepted', models.BooleanField(default=False)),
                ('user_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_receiver_set', to=settings.AUTH_USER_MODEL)),
                ('user_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_sender_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='posteig_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='likeme.Posteig'),
        ),
        migrations.AddField(
            model_name='comments',
            name='user_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]