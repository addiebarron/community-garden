# Generated by Django 3.2.7 on 2021-09-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communitygarden', '0004_alter_soil_water_level'),
    ]

    operations = [
        migrations.CreateModel(
            name='Disconnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('used', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Connection',
        ),
    ]