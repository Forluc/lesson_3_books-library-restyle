import os
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import lxml
import requests
from pathvalidate import sanitize_filename


def parse_book_page(book_number):
    book_data = {
        'title': None,
        'author': None,
        'picture_url': None,
        'url': None,
        'text': None,
        'comments': None,
        'genres': None,
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    base_url = 'https://tululu.org'
    book_data_url = urljoin(base_url, f'b{book_number}/')
    response = requests.get(book_data_url, headers=headers, allow_redirects=True)
    response.raise_for_status()

    if not response.history:
        soup = BeautifulSoup(response.text, 'lxml')

        #  -----------------------------------------title and author-----------------------------------------
        title_and_author = soup.find('table', class_='tabs').find('div', id='content').find('h1')
        separator = title_and_author.text.find('::')
        book_data['title'] = title_and_author.text[:separator].strip()
        book_data['author'] = title_and_author.text[separator + len('::'):].strip()

        #  -----------------------------------------picture_url----------------------------------------------
        picture = soup.find('body').find('div', class_='bookimage').find('img').get('src')
        book_data['picture_url'] = urljoin(base_url, picture)

        #  -----------------------------------------url------------------------------------------------------
        try:
            links = soup.find('div', id='content').find('table').find_all('a')
        except:
            links = None
        for link in links:
            if link.get('href')[:4] == '/txt':
                book_data['url'] = urljoin(base_url, link.get('href'))
                break

        #  -----------------------------------------text-----------------------------------------------------
        book_data['text'] = soup.find('td', class_='ow_px_td').find_all('table', class_='d_book')[1].text

        #  -----------------------------------------comments-------------------------------------------------
        comments = []
        for comment in soup.find('td', class_='ow_px_td').find_all('div', class_='texts'):
            author_and_comment = comment.getText()
            start_comment = author_and_comment.find(')')
            commentary = author_and_comment[start_comment + len(')'):]
            comments.append(commentary)
        book_data['comments'] = comments

        #  -----------------------------------------genres---------------------------------------------------
        genres = []
        for genre in soup.find('span', class_='d_book').find_all('a'):
            genres.append(genre.getText())
        book_data['genres'] = genres

        return book_data


def download_txt(url, filename, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()

    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath
