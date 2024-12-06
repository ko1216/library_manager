import os
import pytest
from unittest.mock import patch
from app.models import Book
from app.services import read_file, write_file

TEST_FILE = 'test_books.json'


@pytest.fixture(autouse=True)
def setup_mock_file():
    """Создаёт тестовые данные для тестов и очищает после завершения."""
    sample_data = [
        {'id': 1, 'title': 'Книга 1', 'author': 'Автор 1', 'year': 2020, 'status': True},
        {'id': 2, 'title': 'Книга 2', 'author': 'Автор 2', 'year': 2019, 'status': False},
    ]
    write_file(sample_data, filename=TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_generate_id():
    """Тест генерации уникального идентификатора."""
    book = Book('Новая книга', 'Тестов', 2021, status=True, filename=TEST_FILE)
    assert book.id == 3


def test_to_dict():
    """Тест преобразования объекта книги в словарь."""
    book = Book('Новая книга', 'Тестов', 2021, status=True, filename=TEST_FILE)
    book_dict = book.to_dict()
    assert book_dict == {
        'id': book.id,
        'title': 'Новая книга',
        'author': 'Тестов',
        'year': 2021,
        'status': True,
    }


def test_save():
    """Тест сохранения книги в файл."""
    Book('Новая книга', 'Тестов', 2022, status=False, filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 3
    assert books[-1]['title'] == 'Новая книга'
    assert books[-1]['status'] is False


def test_show_status():
    """Тест отображения статуса книги."""
    book_available = Book('Эта книга в наличии', 'Тест Ф', 2000, status=True, filename=TEST_FILE)
    book_checked_out = Book('Книги нет', 'Тест Е', 2023, status=False, filename=TEST_FILE)
    assert book_available.show_status() == 'В наличии'
    assert book_checked_out.show_status() == 'Выдана'
