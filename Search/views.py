from django.shortcuts import render
import requests
import json
import csv
from django.http import HttpResponse, JsonResponse


kintamasis = []
resultatai = []
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
    # print(kintamasis)
    return render(request, 'youtube.html', {'query': query, 'suggestions': suggestions})


#Download_CSV
def download_csv(request):
    #print(kintamasis)
    results = kintamasis
    # Set up response as CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Suggestions.csv"'

    # Write data to CSV file
    writer = csv.writer(response)
    writer.writerow(['Keyword','Volume','Competition','Overall'])
    for result in results:
        writer.writerow([result])

    return response
#VidIQ
def details(request):
    suggestions = list(set(kintamasis))
    # suggestions = ['keyword are good', 'keywod']
    resultatai = []

    for term in suggestions:
        if ' ' in term:
            term = term.replace(" ", "+")
        url = f"https://api.vidiq.com/xwords/keyword_search/?term={term}&part=questions&limit=300"
        auth = {
            'authorization': 'Bearer UKP!e728d052-d362-4d96-b5c2-fe3d8c60e002!8dc5e271-13d7-419e-aaa6-7a0c3b25b3e7'}
        response = requests.get(url, headers=auth)
        data = json.loads(response.text)
        print(data)
        competition = round(data['normalized_input_term']['competition'])
        volume = round(data['normalized_input_term']['volume'])
        overall = round(data['normalized_input_term']['overall'])
        estimated_monthly_search = round(data['normalized_input_term']['estimated_monthly_search'])

        # Replace "+" symbol with a space in the term
        term = term.replace("+", " ")

        sarasas = {
            'term': term,
            'competition': competition,
            'overall': overall,
            'estimated_monthly_search': estimated_monthly_search,
            }
        resultatai.append(sarasas)

    context = {
        'resultatai': resultatai,
    }

    # Store the resultatai list in the session
    request.session['resultatai'] = resultatai

    return render(request, 'youtube.html', context=context)





def download_csv(request):
    # Retrieve the resultatai list from the session
    resultatai = request.session.get('resultatai', [])

    # Set up response as CSV file
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Suggestions.csv"'

    # Write data to CSV file
    writer = csv.writer(response)
    writer.writerow(
        ['Keyword', 'Estimated Monthly Search', 'Competition', 'Overall'])
    for result in resultatai:
        keyword = result['term']
        competition = result['competition']
        overall = result['overall']
        estimated_monthly_search = result['estimated_monthly_search']

        writer.writerow(
            [keyword, estimated_monthly_search, competition, overall])

    return response














