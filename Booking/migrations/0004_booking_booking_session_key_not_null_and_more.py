# Generated by Django 4.2.16 on 2025-04-26 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Booking', '0003_booking_email'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='booking',
            index=models.Index(condition=models.Q(('session_key__isnull', False)), fields=['session_key'], name='booking_session_key_not_null'),
        ),
        migrations.AddIndex(
            model_name='schedule',
            index=models.Index(fields=['date', 'time'], name='Booking inf_date_46971d_idx'),
        ),
    ]
