# Generated by Django 2.1.5 on 2019-01-18 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='movie',
            fields=[
                ('movieId', models.CharField(db_column='movieId', max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('year', models.IntegerField(null=True)),
                ('genres', models.ManyToManyField(db_table='movie_genre', related_name='movies', to='reviews.genre')),
            ],
        ),
        migrations.CreateModel(
            name='rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.CharField(max_length=16)),
                ('movieId', models.CharField(max_length=16)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=4)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
