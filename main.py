import requests
import os


def get_books(directory):
    for book_id in range(1, 11):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }
        params = {
            'id': book_id
        }
        url = 'https://tululu.org/txt.php'

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = f'{directory}/book_{book_id}.txt'
        with open(filepath, 'wb') as file:
            file.write(response.content)


def main():
    directory = 'books'
    get_books(directory)


if __name__ == '__main__':
    main()
