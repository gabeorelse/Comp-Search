from django.shortcuts import render
import requests
from django.http import HttpResponse
from .forms import KeyForm

def index(request):
    return render(request, 'book_comps/index.html')

def search_books(request):
    print("Request method:", request.method)
    form = KeyForm()
    if request.method == "POST":
        form = KeyForm(request.POST)
        if form.is_valid():
            key_word = request.POST.get('key_word')
            genre = request.POST.get('genre')
            res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={key_word}+subject:{genre}&orderBy=newest&maxResults=40")

            results = res.json()

            rows = []
    
            for book in results['items']:
                rows.append({'publishedDate': book['volumeInfo']['publishedDate'], 'title': book['volumeInfo']['title']})

            return render(request, 'book_comps/index.html', {'table': rows})


#search_books()