import os
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import lxml
import requests
from pathvalidate import sanitize_filename


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author = soup.find('table', class_='tabs').find('div', id='content').find('h1')
    separator = title_and_author.text.find('::')
    title = title_and_author.text[:separator].strip()
    author = title_and_author.text[separator + len('::'):].strip()

    picture = soup.find('body').find('div', class_='bookimage').find('img').get('src')
    picture_url = urljoin(response.url, picture)

    url_split = urlsplit(picture_url)
    picture_path = url_split.path
    slash_find = picture_path[1:].find('/')
    picture_name = picture_path[slash_find + 2:]

    links = soup.find('div', id='content').find('table').find_all('a')
    for link in links:
        if link.get('href')[:4] == '/txt':
            url = urljoin(response.url, link.get('href'))
            break
        else:
            url = None

    text = soup.find('td', class_='ow_px_td').find_all('table', class_='d_book')[1].text

    comments = []
    for comment in soup.find('td', class_='ow_px_td').find_all('div', class_='texts'):
        author_and_comment = comment.getText()
        start_comment = author_and_comment.find(')')
        commentary = author_and_comment[start_comment + len(')'):]
        comments.append(commentary)

    genres = []
    for genre in soup.find('span', class_='d_book').find_all('a'):
        genres.append(genre.getText())

    book = {
        'title': title,
        'author': author,
        'picture_url': picture_url,
        'url': url,
        'text': text,
        'comments': comments,
        'genres': genres,
        'picture_name': picture_name,
    }
    return book


def download_txt(url, filename, folder='books'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if not response.history:
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
        with open(filepath, 'wb') as file:
            file.write(response.content)
        return filepath


def download_image(url, filename, folder='images'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    if not response.history:
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)
