from django.contrib import admin

from .models import Author, Genre, Book, BookInstance, Language


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
