# Generated by Django 4.2.16 on 2025-04-30 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bonuses', '0001_initial'),
        ('Users', '0002_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='coins',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customuser', to='Bonuses.coin', verbose_name='Мяукоины'),
        ),
    ]
