# Generated by Django 2.2.7 on 2019-12-06 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0003_auto_20191206_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='list_type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='seller',
            name='card_holder_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]