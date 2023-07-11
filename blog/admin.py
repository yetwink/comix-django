from django.contrib import admin
from .models import *
# Register your models here.

class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'count_comics']
    ordering = ['id']

    def count_comics(self, obj):
        if obj.comics_set:
            try:
                return f'{len(obj.comics_set.all())}'
            except:
                return '0'
        else:
            return '0'

    count_comics.short_description = 'Кол-во комиксов'

class VolumeInline(admin.TabularInline):
    model = Volume
    fk_name = 'comics'
    extra = 0

class ChapterInline(admin.TabularInline):
    model = Chapter
    fk_name = 'volume'
    extra = 0

class ComicsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'artist', 'writer', 'views', 'count_volumes', 'count_chapters']
    list_display_links = ['id', 'title']
    inlines = [VolumeInline]

    def count_volumes(self, obj):
        if obj.volume_set:
            return f'{len(obj.volume_set.all())}'
        else:
            return '0'

    def count_chapters(self, obj):
        if obj.volume_set:
            try:
                return str(sum([len(volume.chapter_set.all()) for volume in obj.volume_set.all() if volume.chapter_set]))
            except:
                return '0'
        else:
            return '0'


    count_volumes.short_description = 'Кол-во Томов'
    count_chapters.short_description = 'Кол-во Глав'


class VolumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'comics']
    inlines = [ChapterInline]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Comics, ComicsAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Chapter)
admin.site.register(Picture)
admin.site.register(Profile)