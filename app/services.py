import json
import os

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
