# Generated by Django 2.2.5 on 2019-11-22 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('likeme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likemeuser',
            name='photo',
            field=models.ImageField(default='profiles/profile_default.png', upload_to='profiles/'),
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
    ]
