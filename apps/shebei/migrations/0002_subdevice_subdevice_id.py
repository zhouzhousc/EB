# Generated by Django 2.2.2 on 2019-07-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shebei', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdevice',
            name='subdevice_id',
            field=models.CharField(default='', max_length=100, verbose_name='子设备id'),
        ),
    ]
