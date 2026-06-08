from django.contrib import admin
from django import forms
from .models import Category, Tag, HeritageProject, MediaResource, Exhibition, ExhibitionItem


class MediaResourceInline(admin.TabularInline):
    model = MediaResource
    extra = 1
    fields = ['title', 'media_type', 'file', 'url', 'thumbnail', 'description', 'duration', 'is_primary', 'sort_order']


class ExhibitionItemInline(admin.TabularInline):
    model = ExhibitionItem
    extra = 1
    fields = ['project', 'section_title', 'section_description', 'sort_order']
    autocomplete_fields = ['project']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'level', 'created_at']
    list_filter = ['category_type', 'level']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(HeritageProject)
class HeritageProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'code', 'region', 'status', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'tags']
    search_fields = ['name', 'code', 'region', 'inheritors', 'overview', 'content']
    prepopulated_fields = {'code': ('name',)}
    filter_horizontal = ['tags']
    inlines = [MediaResourceInline]
    autocomplete_fields = ['category']
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'english_name', 'category', 'tags', 'code', 'status')
        }),
        ('传承信息', {
            'fields': ('region', 'inheritors', 'origin_date')
        }),
        ('详细内容', {
            'fields': ('overview', 'history', 'content', 'features', 'value', 'current_situation', 'protection_measures')
        }),
        ('媒体与统计', {
            'fields': ('cover_image', 'view_count')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MediaResource)
class MediaResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'media_type', 'is_primary', 'sort_order', 'uploaded_at']
    list_filter = ['media_type', 'is_primary']
    search_fields = ['title', 'description']
    autocomplete_fields = ['project']


@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'curator', 'status', 'view_count', 'start_date', 'created_at']
    list_filter = ['status', 'start_date']
    search_fields = ['title', 'subtitle', 'description', 'curator']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ExhibitionItemInline]
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'subtitle', 'slug', 'status')
        }),
        ('展陈信息', {
            'fields': ('description', 'curator', 'start_date', 'end_date')
        }),
        ('媒体资源', {
            'fields': ('cover_image', 'banner_image')
        }),
        ('统计', {
            'fields': ('view_count',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExhibitionItem)
class ExhibitionItemAdmin(admin.ModelAdmin):
    list_display = ['exhibition', 'project', 'section_title', 'sort_order']
    list_filter = ['exhibition']
    search_fields = ['section_title', 'section_description']
    autocomplete_fields = ['exhibition', 'project']
