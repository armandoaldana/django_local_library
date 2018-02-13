from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre

def index(request):
    """
    Funcion que muestra la pagina principal del sitio
    """
    # Genera las cantidades de agunos objetos
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.
    # Numero de Generos
    num_genres = Genre.objects.all().count()
    # Numero de libros que contienen la palabra 'el' 
    num_libros_palabra_el = Book.objects.filter(title__icontains='el').count()

    # Numero de visitas a esta pagina.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    # Dibuja la plantilla HTML index.html con los datos en la variable context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,
                 'num_authors':num_authors,'num_genres':num_genres,'num_libros_palabra_el':num_libros_palabra_el,
                 'num_visits':num_visits}, 
    )

from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 4 
    context_object_name = 'lista_libros'   # Nombre para la lista como una variable de plantilla
    queryset = Book.objects.filter(title__icontains='') # Obtiene libros con la palabra '' en el titulo
#    queryset = Book.objects.filter(title__icontains='A')[:3] # Obtiene 5 libros con la palabrea 'A' en el titulo
#    queryset = Book.objects.all # Obtiene todos los libros . Pero no funciona la paginacion.

    template_name = 'catalog/book_list.html'  # Especifica el nombre/ubicación de plantilla
	
class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 4
    context_object_name = 'lista_autores'   # Nombre para la lista como una variable de plantilla
    queryset = Author.objects.filter(last_name__icontains='') # Obtiene con la palabraa '' en el primer nombre
#    queryset = Author.objects.filter(last_name__icontains='A')[:5] # Obtiene 5 autores con la palabrea 'A' en el primer nombre
#    queryset = Author.objects.all # Obtiene todos los autores. Pero no funciona la paginacion.
    template_name = 'catalog/author_list.html'  # Especifica el nombre/ubicación de plantilla.
	
class AuthorDetailView(generic.DetailView):
    model = Author

from django.contrib.auth.mixins import LoginRequiredMixin
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

# Reto
from django.contrib.auth.mixins import PermissionRequiredMixin

class LoanedBooksAllListView(PermissionRequiredMixin,generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 4
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')  

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
#from django.core.urlresolvers import reverse
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

    
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author, Book

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class BookUpdate(UpdateView):
    model = Book
    fields = ['title','author','summary','isbn', 'genre', 'language']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
