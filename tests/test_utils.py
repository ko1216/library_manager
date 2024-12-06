import pytest
import os
from app.services import read_file, write_file
from app.utils import create_book, delete_book, find_books, update_book, list_books

TEST_FILE = 'test_books.json'


@pytest.fixture(autouse=True)
def setup_mock_file():
    """Создаёт тестовые данные для utils.py."""
    sample_data = [
        {'id': 1, 'title': 'Книга 1', 'author': 'Автор 1', 'year': 2020, 'status': True},
        {'id': 2, 'title': 'Книга 2', 'author': 'Автор 2', 'year': 2019, 'status': False},
    ]
    write_file(sample_data, filename=TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_create_book(monkeypatch):
    """Тест создания книги."""
    inputs = iter(['Книга 3', 'Автор 3', '2021'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 3
    assert books[-1]['title'] == 'Книга 3'


def test_delete_book(monkeypatch):
    """Тест удаления книги."""
    monkeypatch.setattr('builtins.input', lambda _: '1')
    delete_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 1
    assert books[0]['id'] == 2


def test_find_books(monkeypatch, capsys):
    """Тест поиска книг."""
    monkeypatch.setattr('builtins.input', lambda _: '1')
    find_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert "Книга 1" in captured.out


def test_update_book(monkeypatch):
    """Тест изменения статуса книги."""
    inputs = iter(['1', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    update_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert books[0]['status'] is False


def test_list_books(capsys):
    """Тест отображения всех книг."""
    list_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert "Книга 1" in captured.out
    assert "Книга 2" in captured.out
