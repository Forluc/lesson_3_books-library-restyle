import os
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
import lxml
import requests
from pathvalidate import sanitize_filename


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author = soup.select_one('.tabs #content h1')
    separator = title_and_author.text.find('::')
    title = title_and_author.text[:separator].strip()
    author = title_and_author.text[separator + len('::'):].strip()

    picture = soup.select_one('body .bookimage img')['src']

    picture_url = urljoin(response.url, picture)

    picture_link = urlsplit(picture_url)
    picture_path = picture_link.path
    picture_name_start = picture_path[1:].find('/')
    picture_name = picture_path[picture_name_start + 2:]

    try:
        book_url = urljoin(response.url, soup.select_one('#content table a[href^="/txt"]')['href'])
    except TypeError:
        book_url = None

    text = soup.select_one('.ow_px_td .d_book:last-of-type td').text

    comments = []
    for comment in soup.select('.ow_px_td .texts'):
        author_and_comment = comment.getText()
        start_comment = author_and_comment.find(')')
        commentary = author_and_comment[start_comment + len(')'):]
        comments.append(commentary)

    genres = [genre.getText() for genre in soup.select('.ow_px_td span.d_book a')]

    book = {
        'title': title,
        'author': author,
        'picture_url': picture_url,
        'book_url': book_url,
        'text': text,
        'comments': comments,
        'genres': genres,
        'picture_name': picture_name,
    }
    return book


def download_txt(url, filename, dest_folder, folder='books'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs(os.path.join(dest_folder, folder), exist_ok=True)
    filepath = os.path.join(dest_folder, folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def download_image(url, filename, dest_folder, folder='images'):
    response = requests.get(url, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)

    os.makedirs(os.path.join(dest_folder, folder), exist_ok=True)
    filepath = os.path.join(dest_folder, folder, filename)
    with open(filepath, 'wb') as file:
        file.write(response.content)
    return filepath


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError
