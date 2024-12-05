import os
import json

FILE_PATH = os.path.join(os.path.dirname(__file__), 'books.json')


def read_file(filename=FILE_PATH, silent=False) -> list:
    """
    Читает данные из JSON файла.
    Проверяет целостность данных, формат и существование файла.
    Возвращает список книг или пустой список в случае ошибки.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError('Ожидается список данных.')
        for item in data:
            if not isinstance(item, dict) or not all(
                key in item for key in ['id', 'title', 'author', 'year', 'status']
            ):
                raise ValueError('Некорректная структура данных.')
        return data
    except FileNotFoundError:
        if not silent:
            print('Файл не найден. Создаётся новый файл.')
        return []
    except json.JSONDecodeError:
        if not silent:
            print('Файл повреждён или не является корректным JSON. Создаётся новый файл.')
        return []
    except ValueError as e:
        if not silent:
            print(f'Ошибка структуры данных: {e}. Создаётся новый файл.')
        return []


def write_file(data: list, filename=FILE_PATH) -> None:
    """
    Записывает данные в JSON файл.
    Обрабатывает ошибки записи.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f'Ошибка при внесении изменений в файл: {e}')


class Book:
    """
    Класс для представления книги в библиотеке
    """

    def __init__(self, title, author, year, status=True) -> None:
        self.id = self.generate_id()
        self.title = title
        self.author = author
        self.year = year
        self.status = status

        self.save()

    def __str__(self) -> str:
        return f'"{self.title}" {self.author}, {self.year} год'

    def __repr__(self) -> str:
        return (f'id: {self.id}\n'
                f'title: {self.title}\n'
                f'author: {self.author}\n'
                f'year: {self.year}\n'
                f'status: {self.show_status()}')

    @staticmethod
    def generate_id() -> int:
        """
        Генерирует уникальный id для новой книги.
        """
        data = read_file(silent=True)
        if not data:
            return 1
        existing_ids = {item['id'] for item in data}
        return max(existing_ids) + 1

    def to_dict(self) -> dict:
        """
        Преобразует объект книги в словарь.
        """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'status': self.status
        }

    def save(self) -> None:
        """
        Сохраняет текущий экземпляр книги в файл JSON.
        """
        books = read_file()
        books.append(self.to_dict())
        write_file(books)

    def show_status(self) -> str:
        """
        Возвращает текущий статус книги в виде строки.
        """
        if self.status:
            return 'В наличии'
        else:
            return 'Выдана'
