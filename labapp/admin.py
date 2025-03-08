from django.contrib import admin
from .models import Service, Booking, Report, TestResult

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'service__name')
    raw_id_fields = ('user', 'service')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'generated_at', 'status')
    list_filter = ('status', 'generated_at')
    search_fields = ('user__username', 'service__name')
    raw_id_fields = ('user', 'service', 'booking', 'reviewed_by')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('report', 'parameter', 'value', 'unit', 'is_abnormal')
    list_filter = ('is_abnormal',)
    search_fields = ('parameter', 'report__user__username')
    raw_id_fields = ('report',)