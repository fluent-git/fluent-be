from django.contrib import admin
import accounts.models as models

# Register your models here.
@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TalkHistory)
class TalkHistoryAdmin(admin.ModelAdmin):
    pass