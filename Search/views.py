from django.shortcuts import render
import requests
import json
import csv
import io
from django.http import HttpResponse

kintamasis = []
def search(request):
    query = request.GET.get('q', '')
    suggestions = []

    if query:
        params = {
            'client': 'firefox',
            'q': query,
            'h1': 'en',
        }
        url = f'http://suggestqueries.google.com/complete/search?hl=en&ds=yt&client=youtube&hjson=t&cp=1&q={query}&format=5&alt='
        resp = requests.get(url, params=params)
        result = resp.json()[1]
        suggestions = result
        all_results = [result]

        suggestion_letters = [
            f'{query} a', f'{query} b', f'{query} c', f'{query} d', f'{query} e', f'{query} g', f'{query} h',
            f'{query} i', f'{query} j', f'{query} k', f'{query} m', f'{query} n', f'{query} o', f'{query} p',
            f'{query} q', f'{query} r', f'{query} s', f'{query} t', f'{query} u', f'{query} v', f'{query} w',
            f'{query} x', f'{query} y', f'{query} z', f'{query} 1', f'{query} 2', f'{query} 3', f'{query} 4',
            f'{query} 5', f'{query} 6', f'{query} 7', f'{query} 8', f'{query} 9', f'{query} 0',
        ]

        for letter in suggestion_letters:
            # create a new dict for each request to avoid overwriting
            params_new = params.copy()
            params_new['q'] = letter
            url_new = f'http://suggestqueries.google.com/complete/search?hl=en&ds=yt&client=youtube&hjson=t&cp=1&q={params_new["q"]}&format=5&alt'
            resp = requests.get(url_new, params=params_new)
            result = resp.json()[1]

            suggestions += result
            all_results.append(result)

        # remove duplicates from the suggestions list
        suggestions = list(set(suggestions))

    context = {
        'query': query,
        'suggestions': list(set(suggestions)),

    }
    global kintamasis
    kintamasis = list(set(suggestions))
    return render(request, 'youtube.html', {'query': query, 'suggestions': suggestions})


#Download_CSV


def download_csv(request):
    print(kintamasis)
    results = kintamasis  # assuming kintamasis() returns a list of strings

    # Set up response as CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="kintamasis_results.csv"'

    # Write data to CSV file
    writer = csv.writer(response)
    writer.writerow(['Results'])
    for result in results:
        writer.writerow([result])

    return response













