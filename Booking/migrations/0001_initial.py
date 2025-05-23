# Generated by Django 4.2.16 on 2025-03-18 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Bonuses', '0001_initial'),
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата посещения')),
                ('time', models.CharField(choices=[('0', '10:00'), ('1', '11:00'), ('2', '12:00'), ('3', '13:00'), ('4', '15:00'), ('5', '16:00'), ('6', '17:00'), ('7', '18:00')], max_length=5, verbose_name='Время посещения')),
                ('cost', models.DecimalField(decimal_places=2, default=400.0, max_digits=5, verbose_name='Стандартная стоимость посещения')),
                ('number_of_places', models.PositiveSmallIntegerField(default=5, verbose_name='Количество мест')),
                ('address', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Main.address', verbose_name='Адресс кафе')),
            ],
            options={
                'verbose_name': 'Информация о посещении',
                'verbose_name_plural': 'Информация о посещених',
                'db_table': 'Booking information',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')),
                ('date', models.DateField(verbose_name='Дата посещения')),
                ('time', models.TimeField(verbose_name='Время посещения')),
                ('cost', models.DecimalField(decimal_places=2, default=200.0, max_digits=5, verbose_name='Cтоимость посещения')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Количество человек')),
                ('session_key', models.CharField(blank=True, max_length=32, null=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name='Статус оплаты')),
                ('phone', models.CharField(verbose_name='номер телефона')),
                ('name', models.CharField(verbose_name='Имя посетителя')),
                ('bonuses', models.IntegerField(default=0, verbose_name='Количество списаных бонусов во время оплаты')),
                ('address', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Main.address', verbose_name='Адресс кафе')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Bonuses.coupon', verbose_name='Куопн')),
            ],
            options={
                'verbose_name': 'Бронь',
                'verbose_name_plural': 'Брони',
                'db_table': 'Booking',
            },
        ),
    ]
