from django.contrib import admin
from .models import Book
from django.utils.safestring import mark_safe

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_authors', 'publisher', 'published_date', 'average_rating')
    list_filter = ('genres', 'language', 'setting_country')
    search_fields = ('title', 'authors', 'isbn', 'publisher')
    filter_horizontal = ()
    readonly_fields = ('cover_image_preview',)
    fieldsets = (
        ('Core Information', {
            'fields': ('title', 'subtitle', 'authors', 'isbn')
        }),
        ('Publication Details', {
            'fields': ('publisher', 'published_date', 'edition', 'page_count', 'language')
        }),
        ('Classification', {
            'fields': ('genres', 'subjects', 'keywords', 'mood_tags', 'age_range')
        }),
        ('Geographic Data', {
            'fields': ('author_countries', 'setting_country')
        }),
        ('Media & Links', {
            'fields': ('cover_image', 'cover_image_preview', 'purchase_links', 'borrow_links')
        }),
        ('Ratings', {
            'fields': ('average_rating',)
        }),
    )

    def display_authors(self, obj):
        return ", ".join(obj.authors)
    display_authors.short_description = 'Authors'

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return mark_safe(f'<img src="{obj.cover_image}" style="max-height: 200px;" />')
        return "No cover image"
    cover_image_preview.short_description = 'Cover Preview'


# Register your models
admin.site.register(Book, BookAdmin)