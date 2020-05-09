from django.shortcuts import render

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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_ger_books': num_ger_books,
    }

    # Render the HTML temlate ,index.html with the data in context
    return render(request, 'index.html', context=context)
