# Generated by Django 3.0.7 on 2020-07-21 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20200721_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_color',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Color'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.Sizes'),
            preserve_default=False,
        ),
    ]
