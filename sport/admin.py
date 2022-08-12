from django.contrib import admin
from sport.models import ComplicatedData, BasicData

class BigDataAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('Basicname',)}
admin.site.register(BasicData, BigDataAdmin)
admin.site.register(ComplicatedData)
