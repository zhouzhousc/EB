from django.contrib import admin

# Register your models here.
from .models import Event_list, Log_list, NoticeManager  # 记得导包


@admin.register(Event_list)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'event_no')

@admin.register(Log_list)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'log_leader')

@admin.register(NoticeManager)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'notice_leader')