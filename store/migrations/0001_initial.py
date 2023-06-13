# Generated by Django 4.1.6 on 2023-06-11 17:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('colour', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('images', models.JSONField(default=list)),
                ('size', models.CharField(choices=[('BIG', 'BIG'), ('MEDIUM', 'MEDIUM'), ('MINI', 'MINI')], default='MINI', max_length=6)),
                ('category', models.CharField(choices=[('BAG', 'BAG'), ('CLOTH', 'CLOTH'), ('FOOTWEAR', 'FOOTWEAR')], default='BAG', max_length=8)),
                ('availability', models.CharField(choices=[('IN_STOCK', 'IN_STOCK'), ('SOLD_OUT', 'SOLD_OUT')], default='IN_STOCK', max_length=8)),
            ],
        ),
    ]
