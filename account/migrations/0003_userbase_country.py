# Generated by Django 4.0.4 on 2022-04-30 06:18

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_userbase_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbase',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2),
        ),
    ]
