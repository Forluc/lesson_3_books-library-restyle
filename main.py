import time
from urllib.parse import urljoin

import requests

from all_func import parse_book_page, download_txt, download_image,get_redirect
import argparse


def get_book(book_number):
    base_url = 'https://tululu.org'
    book_url = urljoin(base_url, f'b{book_number}/')
    response = requests.get(book_url, allow_redirects=True)

    if get_redirect(response):
        book = parse_book_page(response)
        if book:
            download_txt(book['book_url'], book['title'])
            download_image(book['picture_url'], book['picture_name'])
            return book['title'], book['author']


def main():
    parser = argparse.ArgumentParser(
        description='Скрипт предназначен для скачивания книг')
    parser.add_argument('--start_id', help='Начало скачивания книг по ID', default=1, type=int)
    parser.add_argument('--end_id', help='Конец скачивания книг по ID', default=10, type=int)
    args = parser.parse_args()

    books_count = args.end_id - args.start_id
    counter = 0

    while books_count >= counter:
        book_number = args.start_id + counter
        try:
            title, author = get_book(book_number)
            print(f'Книга номер {book_number}\n{title}\n{author}')
            counter += 1
        except (TypeError, requests.exceptions.MissingSchema) as error:
            print(f'Книга номер {book_number}\nERROR: {error}')
            counter += 1
        except requests.exceptions.ConnectionError as error:
            print(f'Книга номер {book_number}\nERROR: {error}')
            time.sleep(5)
        except requests.exceptions.HTTPError as error:
            print(f'Книга номер {book_number}\nERROR: {error}')
            counter += 1
        print()


if __name__ == '__main__':
    main()
