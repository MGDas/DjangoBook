from django.shortcuts import redirect

from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from shop.models import Book
from shop.models import Rewiew

from shop.forms import RewiewForm


class StartPageTemplateView(TemplateView):
    template_name = 'base.html'


class BookListView(ListView):
    template_name = 'shop/book_list.html'
    model = Book
    context_object_name = 'books'


class BookDetailView(DetailView):
    template_name = 'shop/book_detail.html'
    model = Book
    context_object_name = 'book'


class RewiewView(View):

    def post(self, request, pk):
        form = RewiewForm(request.POST)
        book = Book.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.book = book
            form.save()
        return redirect(f"/book/{pk}")
