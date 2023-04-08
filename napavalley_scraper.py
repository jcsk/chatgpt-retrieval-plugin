import requests
from bs4 import BeautifulSoup
import time
import json

def get_blog_urls(soup):
    urls = []
    links = soup.find_all('a', {'class': 'btn btn-normal'}, href=True)
    for link in links:
        urls.append(link['href'])
    return urls

def get_blog_data(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    title_div = soup.find('div', {'class': 'intro-head-title'})
    title = title_div.h1.get_text(strip=True)

    body_div = soup.find('div', {'class': 'section section-white blog-detail'})
    list_share_div = body_div.find('div', {'class': 'list-share'})
    if list_share_div:
        list_share_div.extract()

    body = body_div.get_text(strip=True, separator=' ')

    return {'url': url, 'title': title, 'text': body}

base_url = 'https://www.napavalley.com/blog'
all_blog_data = []

for current_page in range(1, 24):  # Iterate from page 1 to 23, inclusive
    page_url = f'{base_url}/page/{current_page}/'
    print(f'Scraping page {page_url}')
    response = requests.get(page_url)
    html = response.content

    if response.status_code != 200:
        break

    soup = BeautifulSoup(html, 'html.parser')
    blog_urls = get_blog_urls(soup)

    for blog_url in blog_urls:
        print(f'Fetching data from {blog_url}')
        blog_data = get_blog_data(blog_url)
        all_blog_data.append(blog_data)
        time.sleep(1)  # 1-second delay

    time.sleep(1)  # 1-second delay between pages

print('Scraping complete.')

# Save results to a JSON file
with open('napavalley_blog_data.json', 'w') as json_file:
    json.dump(all_blog_data, json_file, indent=4)
