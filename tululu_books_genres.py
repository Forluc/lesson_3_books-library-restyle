from bs4 import BeautifulSoup
import lxml
import requests
from urllib.parse import urljoin


def get_genres(book_number):
    base_url = 'https://tululu.org'
    book_data_url = urljoin(base_url, f'b{book_number}')
    response = requests.get(book_data_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author = soup.find('table', class_='tabs').find('div', id='content').find('h1')
    separator = title_and_author.text.find('::')
    title = f'{book_number}. {title_and_author.text[:separator].strip()}'

    book_genres = []
    genres = soup.find('span', class_='d_book').find_all('a')
    for genre in genres:
        book_genres.append(genre.getText())

    return title, book_genres


def main():
    for book_number in range(1, 11):
        try:
            title, book_genres = get_genres(book_number)
            print('Заголовок:', title)
            print(book_genres)
        except:
            pass


if __name__ == '__main__':
    main()
