from django.contrib import admin

from .models import Duty, DutyResult, Visit


class DutyResultInline(admin.TabularInline):
    model = DutyResult
    extra = 0
    max_num = 5


@admin.register(Duty)
class DutyAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration')
    search_fields = ('name',)


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('number', 'caregiver', 'patient', 'start_date_time', 'end_date_time', 'status')
    list_filter = ('status', 'start_date_time', 'caregiver')
    search_fields = ('number', 'caregiver__username', 'patient__username')
    readonly_fields = ('number',)
    inlines = [DutyResultInline]


@admin.register(DutyResult)
class DutyResultAdmin(admin.ModelAdmin):
    list_display = ('visit', 'duty', 'status')
    list_filter = ('status',)
