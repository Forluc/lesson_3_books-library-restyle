# Парсер онлайн-библиотеки [tululu](https://tululu.org)

Скрипт скачивает книги по идентификатору и сохраняет в папке books, в консоль выводятся данные о скачанной книге, либо
что книги нет.

## Окружение

### Требования к установке

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки
зависимостей:

```bash
pip install -r requirements.txt
``` 

### Функция parse_book_page

Принимает номер книги и собирает с сайта данные о книге

### Функция download_txt

Принимает ссылку на книгу, имя(которым назвать эту книгу) и название папки(куда необходимо сохранить книгу)

## Запуск скрипта для скачивания книг

Запуск на Linux(Python 3) или Windows:

Для скачивания без argparse:

В файле main изменить default на нужное начало и конец скачивания книг

```bash
$ python main.py
```

Для скачивания с argparse:

```bash
$ python main.py  --start_id 20 --end_id 30
```

### Цель проекта

Скрипт написан в образовательных целях на онлайн-курсе [Devman](dvmn.org)
