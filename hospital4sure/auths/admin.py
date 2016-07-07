from django.contrib import admin
from .models import *

# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title","order","type"]


admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(UserProfile)
admin.site.register(Address)
admin.site.register(Document)
admin.site.register(UserDocument)
admin.site.register(Question,QuestionAdmin)
admin.site.register(UserAnswer)
admin.site.register(DisplayCategory)
