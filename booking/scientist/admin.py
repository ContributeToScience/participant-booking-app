from django.contrib import admin

from .models import Research, ResearchEvent, ScientistPaymentRecord, DonateSetting


class EventInline(admin.TabularInline):
    model = ResearchEvent


class ResearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end', 'total_credit', 'is_publish', 'created')
    inlines = [
        EventInline,
    ]


class ScientistPaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('scientist', 'credit', 'description')


class DonateSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


admin.site.register(Research, ResearchAdmin)
admin.site.register(ScientistPaymentRecord, ScientistPaymentRecordAdmin)
admin.site.register(DonateSetting, DonateSettingAdmin)
