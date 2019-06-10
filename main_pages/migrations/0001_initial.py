# Generated by Django 2.1.7 on 2019-06-09 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_pages.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=140, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_phone', models.CharField(blank=True, max_length=140, null=True)),
                ('user_picture', models.ImageField(blank=True, null=True, upload_to=main_pages.models.get_user_picture_path)),
                ('student_groups', models.ManyToManyField(blank=True, to='main_pages.StudentGroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]