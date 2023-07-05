import requests
import os
from pathvalidate import sanitize_filename
from all_func import parse_book_page
import argparse


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def get_book_data(book_number):
    book_data = parse_book_page(book_number)
    download_txt(book_data['url'], book_data['title'])
    return book_data['title'], book_data['author']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', help='Начало скачивания книг по ID', default=1)
    parser.add_argument('--end_id', help='Конец скачивания книг по ID', default=10)
    args = parser.parse_args()

    for book_number in range(int(args.start_id), int(args.end_id) + 1):
        try:
            title, author = get_book_data(book_number)
            print(f'{title}\n{author}')
        except:
            print(f'Книги номер {book_number} не существует')
        print()


if __name__ == '__main__':
    main()
