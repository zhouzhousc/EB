# Generated by Django 2.2.2 on 2019-09-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qudong', '0005_equipmenttemplatertu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmenttemplatertu',
            name='etr_cmd',
        ),
        migrations.AddField(
            model_name='equipmenttemplatertu',
            name='etr_cmdid',
            field=models.CharField(default='', max_length=30, verbose_name='模板下发设备指令id'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmenttemplatertu',
            name='etr_cmdnumber',
            field=models.CharField(default='', max_length=30, verbose_name='模板下发设备寄存器个数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmenttemplatertu',
            name='etr_cmdregister',
            field=models.CharField(default='', max_length=30, verbose_name='模板下发设备寄存器地址'),
            preserve_default=False,
        ),
    ]
