# Generated by Django 2.2.2 on 2019-07-18 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidata', '0002_collectdata_subdevice_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectdata',
            name='subdevice_id',
            field=models.IntegerField(verbose_name='子设备id'),
        ),
    ]
