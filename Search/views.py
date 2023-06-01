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
    return render(request, 'index.html', {'query': query, 'suggestions': suggestions})



#Details
def details(request):
    suggestions = list(set(kintamasis))
    # suggestions = ['keyword are good', 'keywod']
    resultatai = []
    # Iterate over each term in the suggestions list
    for term in suggestions:
        # Replace spaces with '+' in the term if necessary
        if ' ' in term:
            term = term.replace(" ", "+")
        # Construct the API URL with the modified term
        url = f"https://api.vidiq.com/xwords/keyword_search/?term={term}&part=questions&limit=300"
        # Add authorization headers to the request
        auth = {
            'authorization': 'Bearer UKP!e728d052-d362-4d96-b5c2-fe3d8c60e002!8dc5e271-13d7-419e-aaa6-7a0c3b25b3e7'}
        # Send a GET request to the API URL
        response = requests.get(url, headers=auth)
        # Parse the response content as JSON
        data = json.loads(response.text)
        print(data)
        # Extract the competition, overall, and estimated monthly search values from the data
        competition = round(data['normalized_input_term']['competition'])
        overall = round(data['normalized_input_term']['overall'])
        estimated_monthly_search = round(data['normalized_input_term']['estimated_monthly_search'])

        # Replace "+" symbol with a space in the term
        term = term.replace("+", " ")
        # Create a dictionary 'sarasas' with the term and its associated metrics
        sarasas = {
            'term': term,
            'competition': competition,
            'overall': overall,
            'estimated_monthly_search': estimated_monthly_search,
            }
        # Append the 'sarasas' dictionary to the 'resultatai' list
        resultatai.append(sarasas)
    # Create a context dictionary with the 'resultatai' list
    context = {
        'resultatai': resultatai,
    }

    # Store the resultatai list in the session
    request.session['resultatai'] = resultatai
    # Render the 'index.html' template with the context data
    return render(request, 'index.html', context=context)

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


















