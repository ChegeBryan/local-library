import datetime

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm


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
        'num_visits': num_visits,
    }

    # Render the HTML temlate ,index.html with the data in context
    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    paginate_by = 10
    template_name = 'catalog/book_list_temp.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)
        # Create any data add add it to the context
        context['book_count'] = Book.objects.count()
        return context


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    paginate = 10


class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginated_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user).filter(
                status__exact='o').order_by('due_back')


class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    paginated_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(
            status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # if this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with
        # data from the request (binding)

        form = RenewBookForm(request.POST)

        # check if form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # (here we just write to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL
            return HttpResponseRedirect(reverse('borrowed-books'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
