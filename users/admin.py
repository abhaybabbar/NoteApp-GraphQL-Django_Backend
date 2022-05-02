from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import ExtendUser
from django.apps import apps
# Register your models here.
class ExtendUserAdmin(UserAdmin):
    pass
admin.site.register(ExtendUser, ExtendUserAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)
