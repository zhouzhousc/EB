# Generated by Django 2.2.2 on 2019-07-18 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shebei', '0001_initial'),
        ('qudong', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modbusrtumodel',
            name='subdevice_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shebei.SubDevice', verbose_name='子设备id'),
            preserve_default=False,
        ),
    ]
