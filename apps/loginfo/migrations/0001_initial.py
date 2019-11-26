# Generated by Django 2.2.2 on 2019-11-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('event_no', models.CharField(max_length=30, verbose_name='序號')),
                ('event_leader', models.CharField(max_length=30, verbose_name='用戶名')),
                ('event_info', models.CharField(max_length=100, verbose_name='事件詳情')),
                ('event_create_time', models.CharField(max_length=30, verbose_name='記錄時間')),
                ('event_type', models.CharField(max_length=30, verbose_name='事件類型')),
            ],
            options={
                'db_table': 'gateway_event_list',
                'verbose_name_plural': '事件中心',
                'verbose_name': '事件中心',
            },
        ),
        migrations.CreateModel(
            name='Log_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('log_type', models.CharField(max_length=30, verbose_name='文件名')),
                ('log_leader', models.CharField(max_length=30, verbose_name='管理者')),
                ('log_level', models.CharField(max_length=30, verbose_name='日志级别')),
                ('log_info', models.CharField(max_length=30, verbose_name='描述')),
                ('log_no', models.SmallIntegerField(choices=[(1, '系统日志'), (2, '采集日志'), (3, '传输日志'), (4, '网络日志'), (5, '权限日志')], default=0, verbose_name='日志类型')),
            ],
            options={
                'db_table': 'gateway_log_list',
                'verbose_name_plural': '日志中心',
                'verbose_name': '日志中心',
            },
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=30, verbose_name='名字')),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'gateway_name',
                'verbose_name_plural': '測試',
                'verbose_name': '測試',
            },
        ),
        migrations.CreateModel(
            name='NoticeManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('notice_leader', models.CharField(max_length=30, verbose_name='責任人')),
                ('notice_location', models.CharField(max_length=30, verbose_name='地點')),
                ('notice_message_num', models.CharField(max_length=30, verbose_name='消息數據')),
                ('notice_time', models.CharField(max_length=30, verbose_name='時間')),
                ('notice_status', models.IntegerField()),
                ('notice_phone', models.CharField(max_length=30, verbose_name='電話')),
                ('notice_email', models.CharField(max_length=50, verbose_name='郵箱')),
            ],
            options={
                'db_table': 'gateway_notice_manager',
                'verbose_name_plural': '通知管理',
                'verbose_name': '通知管理',
            },
        ),
    ]
