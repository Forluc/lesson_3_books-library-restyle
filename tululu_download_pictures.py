import os.path

from bs4 import BeautifulSoup
import lxml
import requests
from urllib.parse import urljoin, urlsplit


def get_book_picture(book_number):
    base_url = 'https://tululu.org'

    book_data_url = urljoin(base_url, f'b{book_number}')
    response = requests.get(book_data_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    picture = soup.find('body').find('div', class_='bookimage').find('img').get('src')
    picture_url = urljoin(base_url, picture)
    url_split = urlsplit(picture_url)
    picture_path = url_split.path

    slash_find = picture_path[1:].find('/')

    picture_name = picture_path[slash_find + 2:]

    return download_picture(picture_url, picture_name)


def download_picture(picture_url, picture_name, folder='images'):
    response = requests.get(picture_url)
    response.raise_for_status()

    if not os.path.exists('images'):
        os.makedirs('images')

    filepath = os.path.join(folder, picture_name)
    with open(filepath, 'wb') as file:
        file.write(response.content)


def main():
    for book_number in range(1, 11):
        try:
            get_book_picture(book_number)
        except:
            pass


if __name__ == '__main__':
    main()
