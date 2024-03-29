# Generated by Django 2.2.7 on 2019-12-06 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(max_length=100, null=True)),
                ('password', models.CharField(default='', max_length=20)),
                ('phone_num', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'Member',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_price', models.FloatField(default=0.0)),
                ('order_date', models.DateField(null=True)),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('gift', models.CharField(max_length=10, null=True)),
                ('billing_addr', models.CharField(default='', max_length=10)),
                ('paid_date', models.DateField(null=True)),
                ('card', models.IntegerField(default=0)),
                ('discount', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'Payment',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('stock', models.IntegerField(default=0)),
                ('descript', models.CharField(default='', max_length=500)),
                ('product_name', models.CharField(default='', max_length=200)),
                ('brand', models.CharField(max_length=100, null=True)),
                ('price', models.FloatField(default=0.0)),
                ('discount', models.IntegerField(null=True)),
                ('order', models.ManyToManyField(db_table='Includes', related_name='Order_ID', to='amazon.Order')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('shipping_id', models.AutoField(primary_key=True, serialize=False)),
                ('addr', models.CharField(max_length=100)),
                ('ship_date', models.DateField(null=True)),
                ('method', models.CharField(max_length=50)),
                ('courier', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'Shipment',
            },
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='amazon.Member')),
                ('membership_stt', models.IntegerField(default=0)),
                ('default_addr', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'Buyer',
            },
            bases=('amazon.member',),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('member_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='amazon.Member')),
                ('seller_phone_num', models.CharField(default='', max_length=20)),
                ('address', models.CharField(default='', max_length=100)),
                ('country', models.CharField(default='', max_length=20)),
                ('card_num', models.CharField(default='', max_length=20)),
                ('card_expr_date', models.DateField()),
                ('card_holder_name', models.CharField(default='', max_length=100)),
                ('zip_code', models.CharField(max_length=20, null=True)),
                ('company_name', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'Seller',
            },
            bases=('amazon.member',),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Shipment'),
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(default='', max_length=100)),
                ('category', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Category')),
                ('contains', models.ManyToManyField(db_table='Contains', to='amazon.Product')),
            ],
            options={
                'db_table': 'Subcategory',
                'unique_together': {('subcategory_name', 'category')},
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('cmt', models.CharField(default='', max_length=500)),
                ('rating', models.IntegerField(null=True)),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Product')),
                ('buyer', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Buyer')),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Product_picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Product')),
            ],
            options={
                'db_table': 'Product_Picture',
                'unique_together': {('product', 'image')},
            },
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Seller'),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('order_id', 'shipping', 'payment')},
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('name', models.AutoField(primary_key=True, serialize=False)),
                ('privacy', models.CharField(choices=[('Pub', 'Public'), ('Pri', 'Private')], default='Pri', max_length=3)),
                ('list_type', models.CharField(default='', max_length=20)),
                ('member', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Member')),
            ],
            options={
                'db_table': 'List',
                'unique_together': {('member', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='friend', to='amazon.Member')),
                ('member', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='member', to='amazon.Member')),
            ],
            options={
                'db_table': 'Friend',
                'unique_together': {('member', 'friend')},
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=100, null=True)),
                ('product', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Product')),
            ],
            options={
                'db_table': 'Feature',
                'unique_together': {('product', 'feature')},
            },
        ),
        migrations.AddField(
            model_name='buyer',
            name='order',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Order'),
        ),
        migrations.CreateModel(
            name='Refunds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Order')),
                ('product', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Product')),
                ('buyer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Buyer')),
            ],
            options={
                'db_table': 'Refunds',
                'unique_together': {('order', 'product')},
            },
        ),
        migrations.CreateModel(
            name='Buyer_optional_addr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optional_addr', models.CharField(max_length=100, null=True)),
                ('buyer', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='amazon.Buyer')),
            ],
            options={
                'db_table': 'Buyer_Optional_Addr',
                'unique_together': {('buyer', 'optional_addr')},
            },
        ),
        migrations.CreateModel(
            name='Buyer_card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_number', models.CharField(default='', max_length=20)),
                ('card_holder_name', models.CharField(default='', max_length=50)),
                ('card_expr_date', models.DateField()),
                ('account', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='amazon.Buyer')),
            ],
            options={
                'db_table': 'Buyer_Card',
                'unique_together': {('account', 'card_number')},
            },
        ),
    ]
