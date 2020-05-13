from django.shortcuts import render
from django.views import generic
from django.views.generic import ListView, DetailView

from catalog.models import Book, Author, BookInstance, Genre


def index(request):
    """ View function for home page of site """

    # Generate cunts of the some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Availbale books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Books (title contains 'Ger') ignore case
    num_ger_books = Book.objects.filter(title__icontains='ger').count()

    # Count Genres (name contains 'fic')
    num_fic_genres = Genre.objects.filter(name__icontains='fic').count()

    # NUmber of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_ger_books': num_ger_books,
        'num_fic_genres': num_fic_genres,
    }

    # Render the HTML temlate ,index.html with the data in context
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    template_name = 'catalog/book_list_temp.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data add add it to the context
        context['book_count'] = Book.objects.count()
        return context


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    paginate = 10


class AuthorDetailView(DetailView):
    model = Author
