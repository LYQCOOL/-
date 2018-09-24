from django.contrib import admin
from user import models

# Register your models here.
class useradmin(admin.ModelAdmin):
    list_display =('pk','username','user_role',)
admin.site.register(models.User,useradmin)
admin.site.register(models.Class)
admin.site.register(models.S_class)
admin.site.register(models.kaoqing)
