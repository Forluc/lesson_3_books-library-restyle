import time
from urllib.parse import urljoin

import requests

from all_func import parse_book_page, download_txt, download_image
import argparse


def get_book(book_number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    base_url = 'https://tululu.org'
    book_data_url = urljoin(base_url, f'b{book_number}/')
    response = requests.get(book_data_url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    if not response.history:
        book = parse_book_page(response)
        if book:
            download_txt(book['url'], book['title'])
            download_image(book['picture_url'], book['picture_name'])
            return book['title'], book['author']


def main():
    parser = argparse.ArgumentParser()
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
