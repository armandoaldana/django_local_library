from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language

admin.site.register(Language)
admin.site.register(Genre)

class BookInline(admin.TabularInline):
    model = Book
    extra = 0

#admin.site.register(Author)
# Define the admin class - Reemplaza la linea anterior - admin.site.register(Author)
# Se cambia la presentacion por defecto del modelo (Author en este caso) en la interface de administracion
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0
    
#admin.site.register(Book)
@admin.register(Book)  # Tiene el mismo efecto que: admin.site.register(Book, BookAdmin)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'nombre_genero')
    inlines = [BooksInstanceInline]

# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        ('Basicos', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Disponibilidad', {
            'fields': ('status', 'due_back', 'borrower')
        }),
     )
