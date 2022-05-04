from django.contrib import admin
from .models import Labels, Notes
# Register your models here.
@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'slug')
    search_fields = ('user', 'label')
    
@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'created_at', 'slug']
    search_fields = ['user__username', 'title', 'slug']