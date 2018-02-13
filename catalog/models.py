from django.db import models

# Create your models here.

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

# Clase Genero
class Genre(models.Model):
    """
    Modelo que representa el genero el libro. Ej: Ciencia ficcion, Policiaca, Aventura, Romance, etc.
    """
    name = models.CharField(max_length = 200, verbose_name = "Nombre de Genero",
           help_text = "Entre el genero del libro. Ej: Ciencia ficcion, Policiaca, Aventura, Romance, etc.)" )
    
    def __str__(self):
        """
        Cadena para representar el objeto (en el sitio de administración, etc.)
        """
        return self.name

class Language(models.Model):
    """
    Modelo que representa el Lenguage (Ej: Ingles, Frances, Japones, etc.)
    """
    name = models.CharField(max_length=200, verbose_name = "Nombre Lenguaje", help_text="Entre el lenguaje natural del libro. (Ej: Ingles, Frances, Japanes, etc)")
    
    def __str__(self):
        """
        Cadena para representar el objeto (en el sitio de administración, etc.)
        """
        return self.name

# Clase Libro
class Book(models.Model):
    """
    Modelo que representa un libro(pero no la instancia del libro.)
    """
    title = models.CharField(max_length=200, verbose_name = "Titulo", help_text="Entre el titulo del libro")
    # Author - Clave foranea. Se usa porque el libro solo puede tener un autor, pero los autores pueden tener varios libros
    # Author como una cadena en lugar de un objeto porque todavía no se ha declarado en el archivo.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name = "Autor", help_text="Seleccione el nombre del autor")
    summary = models.TextField(max_length=1000, verbose_name = "Descripcion", help_text="Entre una breve descripcion del libro.")
    # Enlace a la pagina de: International ISBN Agency
    isbn = models.CharField('ISBN',max_length=13, help_text='Entre 13 Caracteres de <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField se usa porque un libro puede tener muchos generos. Los libros pueden abarcar muchos generos.
    # La clase Genre ya se definio.
    genre = models.ManyToManyField(Genre, verbose_name="Genero", help_text="Seleccione un genero para el libro.")
    language = models.ForeignKey('Language', verbose_name ="Lenguaje", on_delete=models.SET_NULL, null=True, help_text="Entre el Lenguaje")
    
    def nombre_genero(self):
        """
        Crea una cadena para el Genero. Esto es requerido para desplegar el genero en Interface Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
        display_genre.short_description = 'Genero'

    def get_absolute_url(self):
        """
        Devuelve la url para acceder a una instancia de un libro en particular.
        """
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """
        Cadena para representar el objeto (en el sitio de administración, etc.)
        """
        return self.title

# Clase Instancias del Libro
import uuid # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User # Requirido para asignar a un usuario un prestamo

class BookInstance(models.Model):
    """
    Modelo que representa una copia especifica de un libro(Ej: Libro que puede ser prestado).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, verbose_name = "ID",
         help_text="ID unico para el libro en toda la Libreria")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, verbose_name = "Libro", help_text="Seleccione el libro", null=True) 
    imprint = models.CharField(max_length=200, verbose_name = "Version", help_text="Entre la version")
    due_back = models.DateField(null=True, blank=True, verbose_name = "Fecha reintegro", help_text="Entre la fecha de reintegro")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Mantenimiento'),
        ('o', 'Prestado'),
        ('a', 'Disponible'),
        ('r', 'Reservado'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', verbose_name = "Disponibilidad", help_text='Seleccione la Disponibilidad')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        
    def __str__(self):
        """
        Cadena para representar el objeto (en el sitio de administración, etc.)
        """
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
	
# Clase Autor del Libro (se asume un autor por libro)
class Author(models.Model):
    """
    Modelo que representa el autor.
    """
    first_name = models.CharField(max_length=100, verbose_name = "Primer Nombre")
    last_name = models.CharField(max_length=100, verbose_name = "Segundo Apellido")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name = "Fecha Nacimiento")
    date_of_death = models.DateField('Fallecido', null=True, blank=True)
    
    def get_absolute_url(self):
        """
        Returna el url para acceder a una instancia del autor.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)
