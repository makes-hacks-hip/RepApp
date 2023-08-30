from django.contrib import admin
from .models import Attachment, Message


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'mime_type']
    list_filter = ['owner', 'mime_type']
    search_fields = ['name', 'owner']
    ordering = ['owner', 'name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['receiver', 'summary',
                    'sender', 'created', 'sent', 'answered']
    list_filter = ['receiver', 'sender', 'created', 'sent', 'answered']
    search_fields = ['receiver', 'summary', 'sender']
    date_hierarchy = 'created'
    ordering = ['-created', 'receiver']
