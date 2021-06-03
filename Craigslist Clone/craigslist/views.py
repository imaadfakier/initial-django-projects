from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

# BASE_CRAIGSLIST_URL = 'https://capetown.craigslist.org/search/?query={}'
BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    Search.objects.create(search=search)
    # print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    # print(final_url)
    response = requests.get(final_url)
    data = response.text
    # print(data)
    # print(search)

    soup = BeautifulSoup(data, features='html.parser')

    # post_titles = soup.findAll('a', {'class':'result-title'})
    # print(post_titles)
    # print(post_titles[0])
    # print(post_titles[0].text)
    # print(post_titles[0].text.get('href'))

    post_listings = soup.findAll('li', {'class': 'result-row'})
    # post_title = post_listings[0].find(class_='result-title').text
    # post_url = post_listings[0].find('a').get('href')
    # post_price = post_listings[0].find(class_='result-price').text
    # print(post_title)
    # print(post_url)
    # print(post_price)

    # Post Image
    # ...

    final_postings = []

    for post in post_listings:
        if post.find(class_='result-image').get('data-ids'):
            # post_image = post.find(class_ = 'result-image').get('data-ids')[0]
            # post_image = post.find(class_='result-image').get('data-ids')
            # print(post_image)
            # post_image = post.find(class_='result-image').get('data-ids').split(',')[0]
            # print(post_image)
            # post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split('1:')
            # post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')
            post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            # print(post_image)
            post_image_url = BASE_IMAGE_URL.format(post_image)
            # print(post_image)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpeg'

        post_title = post.find(class_='result-title').text[:100]
        post_url = post.find('a').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        # if post.find(class_='result-image').get('data-ids'):
        #     # post_image = post.find(class_ = 'result-image').get('data-ids')[0]
        #     # post_image = post.find(class_='result-image').get('data-ids')
        #     # print(post_image)
        #     # post_image = post.find(class_='result-image').get('data-ids').split(',')[0]
        #     # print(post_image)
        #     # post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split('1:')
        #     # post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')
        #     post_image = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
        #     # print(post_image)
        #     post_image_url = BASE_IMAGE_URL.format(post_image)
        #     # print(post_image)
        # else:
        #     post_image_url = 'https://craigslist.org/images/peace.jpeg'

        final_postings.append((post_image_url, post_title, post_url, post_price))

    # stuff_for_frontend = {
    #     'search':search,
    # }
    stuff_for_frontend = {
        'search': search,
        'final_postings':final_postings,
    }
    return render(request, 'craigslist/new_search.html', context=stuff_for_frontend)