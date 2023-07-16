from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import lxml


def get_book_link(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    links = soup.find('body').find_all('table', class_='d_book')
    books_urls = []
    for link in links:
        books_urls.append(urljoin(url, link.find('a')['href']))
    return books_urls


def main():
    url = 'https://tululu.org/l55/'
    print(*get_book_link(url), sep='\n')


if __name__ == '__main__':
    main()
