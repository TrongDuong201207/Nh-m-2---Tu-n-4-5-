from django.contrib import admin
from .models import GradeComponent, Grade

@admin.register(GradeComponent)
class GradeComponentAdmin(admin.ModelAdmin):
    list_display = ('course_section', 'component_name', 'weight_percent', 'position')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'component', 'score', 'updated_by', 'updated_at')
    list_filter = ('component__course_section',)
