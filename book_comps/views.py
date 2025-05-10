from django.shortcuts import render
import requests
from django.http import HttpResponse
from .forms import KeyForm
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil import parser
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def parse_date(date_string):
    try:
        return parser.parse(date_string)
    except (parser.ParserError, TypeError):
        return None


def index(request):
    return render(request, 'book_comps/index.html')

def search_books(request):
    print("Request method:", request.method)
    form = KeyForm()
    if request.method == "POST":
        form = KeyForm(request.POST)
        if form.is_valid():

            max_results = 40
            start_index = 0
            
            current_time = datetime.now()
            minus = relativedelta(years=5)

            limit = current_time - minus

            while True:
                key_word = quote_plus(request.POST.get('key_word'))
                genre = quote_plus(request.POST.get('genre'))
                url = f"https://www.googleapis.com/books/v1/volumes?q={key_word}+{genre}+subject:fiction&startIndex={start_index}&maxResults={max_results}&printType=books"
                try: 
                    response = requests.get(url)
                    response.raise_for_status()
                    results = response.json()
                    print(results)
                    
                    rows = []
                    for book in results['items']:
                        # pulls date as a string
                        date = book['volumeInfo'].get('publishedDate')
                        print(date)
                        # calls parse_date function to change date to datetime format
                        correct_date = parse_date(date)
                        if correct_date is None:
                            continue
                        if correct_date >= limit:
                            rows.append({'publishedDate': book['volumeInfo']['publishedDate'], 'title': book['volumeInfo']['title'], 'authors': book['volumeInfo']['authors']})
                            if 'authors' == None:
                                rows.append({'publishedDate': book['volumeInfo']['publishedDate'], 'title': book['volumeInfo']['title']})
                                continue
                            if 'title' == None:
                                continue
                            if len(rows) >= 100:
                                break
                            if "totalItems" in results:
                                total_items = results["totalItems"]
                                if start_index + max_results >= total_items:
                                    break
                            else:
                                break

                    start_index += max_results
                    print(rows)
                    
                    df = pd.DataFrame(rows)
                    context = df.to_html()
                    with open("book_comps/search_books.html", "w", encoding="utf-8") as text_file:
                        text_file.write(context)
                    return render(request, 'book_comps/search_books.html', {'table': context})
                    
                
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")

def goodreads_search():

    rows = [{'publishedDate': '2025-04-15', 'title': 'The Dagger and the Flame', 'authors': ['Ana Bidault', 'Elena Bonotto', 'Hannah Konetzki', 'Paule Ledesma', 'Eeva Nikunen']}, {'publishedDate': '2024-07-30', 'title': 'A Power Unbound', 'authors': ['Elodie Now']}]
    for row in rows:
        url = f"https://www.google.com/search?q={row['title'].replace(' ', '+')}"
        try: 
            response = requests.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            soup.prettify()

            star_rating = []
            rating = soup.find("div", class_="gsrt KMdzJ")
            print(rating.text.strip())
            shelves = soup.find("span", class_="RDApEe YrbPuc")
            star_rating.append({'Star Rating' : rating, 'Rating Count' : shelves})

            print(star_rating)


        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")


goodreads_search()