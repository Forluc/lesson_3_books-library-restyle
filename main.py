from all_func import parse_book_page, download_txt
import argparse


def get_book_data(book_number):
    book_data = parse_book_page(book_number)
    if book_data:
        download_txt(book_data['url'], book_data['title'])
        return book_data['title'], book_data['author']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', help='Начало скачивания книг по ID',
                        default=1)  # Изменить default на нужное начало скачивания книг
    parser.add_argument('--end_id', help='Конец скачивания книг по ID',
                        default=10)  # Изменить default на нужный конец скачивания книг
    args = parser.parse_args()

    for book_number in range(int(args.start_id), int(args.end_id) + 1):
        try:
            title, author = get_book_data(book_number)
            print(f'{title}\n{author}')
        except:
            print(f'Книги номер {book_number} не существует, либо нет ссылки на скачивание')
        print()


if __name__ == '__main__':
    main()
