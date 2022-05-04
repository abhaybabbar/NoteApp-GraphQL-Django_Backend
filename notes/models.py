from django.db import models
from django.utils.translation import gettext_lazy  as _
from django.conf import settings
from autoslug import AutoSlugField

# Create your models here.
class Labels(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    label = models.CharField(_('Labels'), max_length=255)
    slug = AutoSlugField(populate_from='label', unique_with=['user'], null=True, always_update=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.label}'
    
    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
        unique_together = ('user', 'label')
        
class Notes(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='note_user', on_delete=models.CASCADE, blank=False)
    title = models.CharField(_('Note Title'), max_length=255, blank=False)
    content = models.TextField(_("Note Content"), blank=True)
    labels = models.ManyToManyField(Labels, related_name='note_label', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='title', unique_with=['user'], always_update=True)
    
    def __str__(self):
        return f'{self.user.username}, {self.title}'
    
    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
    
    