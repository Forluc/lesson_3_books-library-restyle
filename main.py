import requests
from bs4 import BeautifulSoup
import lxml
import os
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    base_url = 'https://tululu.org'
    book_data_url = urljoin(base_url, f'b{book_number}')
    response = requests.get(book_data_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    for a in soup.find('div', id='content').find('table').find_all('a'):
        if a.get('href')[:4] == '/txt':  # Проверяет, есть ли ссылка на книгу
            book_url = urljoin(base_url, a.get('href'))
            break

    title_and_author = soup.find('table', class_='tabs').find('div', id='content').find('h1')
    separator = title_and_author.text.find('::')

    title = f'{book_number}. {title_and_author.text[:separator].strip()}'

    download_txt(book_url, title)


def main():
    for book_number in range(1, 11):
        try:
            get_book_data(book_number)
            print(f'Книга с номером {book_number} скачана')
        except:
            print(f'Книги номер {book_number} не существует')


if __name__ == '__main__':
    main()
