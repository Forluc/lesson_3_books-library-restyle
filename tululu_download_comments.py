from bs4 import BeautifulSoup
import lxml
import requests
from urllib.parse import urljoin


def get_comments(book_number):
    base_url = 'https://tululu.org'
    book_data_url = urljoin(base_url, f'b{book_number}')
    response = requests.get(book_data_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author = soup.find('table', class_='tabs').find('div', id='content').find('h1')
    separator = title_and_author.text.find('::')
    title = title_and_author.text[:separator].strip()

    commentaries = []

    comments = soup.find('td', class_='ow_px_td').find_all('div', class_='texts')
    for comment in comments:
        author_and_comment = comment.getText()
        start_comment = author_and_comment.find(')')
        commentary = author_and_comment[start_comment + len(')'):]
        commentaries.append(commentary)
    return title, commentaries


def main():
    for book_number in range(1, 11):
        try:
            title, commentaries = get_comments(book_number)
            print(title)
            if commentaries:
                for commentary in commentaries:
                    print(commentary)
            else:
                print()
        except:
            pass


if __name__ == '__main__':
    main()
