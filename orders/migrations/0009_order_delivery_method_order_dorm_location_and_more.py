# Generated by Django 5.1.6 on 2025-04-07 19:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(blank=True, choices=[('pickup', 'Pickup'), ('dorm', 'Dorm')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='dorm_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('meal_swipe', 'Meal Swipe'), ('flex_dollars', 'Flex Dollars')], max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_swipes', models.IntegerField(default=250)),
                ('flex_dollars', models.DecimalField(decimal_places=2, default=150.0, max_digits=6)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
