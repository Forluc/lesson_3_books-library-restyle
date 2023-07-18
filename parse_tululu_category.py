import argparse
import json
import time
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup
import lxml
from all_func import parse_book_page, download_txt, download_image, check_for_redirect


def get_books_links(page_number):
    url = f'https://tululu.org/l55/{page_number}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')

    links = soup.select('body .d_book')
    books_urls = [urljoin(url, link.select_one('a')['href']) for link in links]
    return books_urls


def get_book(url):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    book = parse_book_page(response)

    img_src = download_image(book['picture_url'], book['picture_name'])
    book_path = download_txt(book['book_url'], book['title'])

    book_description = {
        'title': book['title'],
        'author': book['author'],
        'img_src': img_src,
        'book_path': book_path,
        'comments': book['comments'],
        'genres': book['genres'],
    }
    return book_description


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт предназначен для скачивания книг')
    parser.add_argument('--start_page', help='Страница начала скачивания книг', default=1, type=int)
    parser.add_argument('--end_page', help='Страница конца скачивания книг', default=4, type=int)
    args = parser.parse_args()

    links = []
    for page_number in range(args.start_page, args.end_page + 1):
        try:
            links.extend(get_books_links(page_number))
        except requests.exceptions.HTTPError:
            print(f'ERROR: На странице номер {page_number} произошел редирект')

    counter = 0
    books_descriptions = []
    for link in links:
        book_number = urlsplit(link).path[2:-1]
        try:
            books_descriptions.append(get_book(link))
            print(f'Книга номер {book_number} скачана')
            counter += 1
        except (TypeError, requests.exceptions.MissingSchema) as error:
            print(f'Книга номер {book_number}\nERROR: {error}')
            counter += 1
        except requests.exceptions.ConnectionError as error:
            print(f'Книга номер {book_number}\nERROR: {error}')
            time.sleep(5)
        except requests.exceptions.HTTPError:
            print(f'Книга номер {book_number}\nERROR: Произошел редирект')
            counter += 1
        print()

    with open('books_descriptions.json', 'w', encoding='utf-8') as file:
        json.dump(books_descriptions, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
