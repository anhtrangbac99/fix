# Generated by Django 2.2.7 on 2019-12-08 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amazon', '0004_auto_20191206_1705'),
    ]

    operations = [
        migrations.RenameField(
            model_name='list',
            old_name='name',
            new_name='list_name',
        ),
        migrations.RenameField(
            model_name='seller',
            old_name='company_name',
            new_name='comp_name',
        ),
        migrations.AlterField(
            model_name='list',
            name='privacy',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='zip_code',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='list',
            unique_together={('account', 'list_name')},
        ),
        migrations.CreateModel(
            name='ConsistOf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_list', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.List')),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Product')),
            ],
            options={
                'db_table': 'ConsistOf',
            },
        ),
    ]
