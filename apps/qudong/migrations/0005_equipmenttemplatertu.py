# Generated by Django 2.2.2 on 2019-09-12 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qudong', '0004_auto_20190718_1132'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentTemplateRtu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('etr_name', models.CharField(max_length=30, verbose_name='模板名称')),
                ('etr_remark', models.CharField(max_length=30, verbose_name='模板描述')),
                ('etr_accordname', models.CharField(default='ModeBus-RTU', max_length=30, verbose_name='模板协议名称')),
                ('etr_cmd', models.CharField(max_length=50, verbose_name='模板下发设备指令')),
                ('etr_param', models.CharField(max_length=50, verbose_name='模板返回设备数据的参数名')),
                ('etr_format', models.SmallIntegerField(choices=[(0, 'Hex'), (1, '长整型'), (2, 'IEE-754')], default=0, verbose_name='模板返回设备数据格式')),
                ('etr_rule', models.CharField(max_length=30, verbose_name='模板返回数据计算公式')),
            ],
            options={
                'verbose_name_plural': 'ModBusRtu设备模板库',
                'verbose_name': 'ModBusRtu设备模板库',
                'db_table': 'gateway_equipmenttemplatertu',
            },
        ),
    ]
