# Generated by Django 4.1.7 on 2023-03-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('neoble', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_updated', models.CharField(max_length=255)),
                ('auctions', models.JSONField()),
            ],
        ),
    ]
