# Generated by Django 3.1.2 on 2020-10-22 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0057_auto_20201022_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hodan',
            name='created_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Ngày tạo'),
        ),
    ]
