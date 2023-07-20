import argparse
import json
import os
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


def get_book_with_description(url, dest_folder, skip_imgs, skip_txt):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    book = parse_book_page(response)

    img_src = None if skip_imgs else download_image(book['picture_url'], book['picture_name'], dest_folder)
    book_path = None if skip_txt else download_txt(book['book_url'], book['title'], dest_folder)

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
    parser.add_argument('--start_page', help='Страница начала скачивания книг', default=700, type=int)
    parser.add_argument('--end_page', help='Страница конца скачивания книг', default=701, type=int)
    parser.add_argument('--dest_folder', help='Путь к каталогу с результатами парсинга: картинкам, книгам, JSON',
                        default='files')
    parser.add_argument('--skip_imgs', help='Не скачивать картинки', action='store_true',
                        default=False)
    parser.add_argument('--skip_txt', help='Не скачивать книги', action='store_true', default=False)
    args = parser.parse_args()

    os.makedirs(args.dest_folder, exist_ok=True)

    counter = 0
    page_count = args.end_page - args.start_page
    links = []

    while page_count >= counter:
        try:
            links.extend(get_books_links(args.start_page + counter))
            counter += 1
        except requests.exceptions.HTTPError:
            print(f'ERROR: На странице номер {args.start_page + counter} произошел редирект')
            counter += 1
        except requests.exceptions.ConnectionError as error:
            print(error)
            time.sleep(5)

    books_count = len(links)
    counter = 0
    books_descriptions = []
    while books_count > counter:
        book_number = urlsplit(links[counter]).path[2:-1]
        try:
            books_descriptions.append(
                get_book_with_description(links[counter], args.dest_folder, args.skip_imgs, args.skip_txt))
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

    with open(os.path.join(args.dest_folder, 'books_descriptions.json'), 'w', encoding='utf-8') as file:
        json.dump(books_descriptions, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
