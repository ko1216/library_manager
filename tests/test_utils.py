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


def test_create_book_empty_title(monkeypatch, capsys):
    """Тест создания книги с пустым названием."""
    inputs = iter(['', 'Книга 3', 'Автор 3', '2021'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_book(filename=TEST_FILE)
    captured = capsys.readouterr()
    books = read_file(filename=TEST_FILE)
    assert 'Название книги не может быть пустым.' in captured.out
    assert len(books) == 3
    assert books[-1]['title'] == 'Книга 3'


def test_create_book_invalid_year(monkeypatch):
    """Тест создания книги с некорректным годом."""
    inputs = iter(['Книга 3', 'Автор 3', 'ааа', '2021'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    create_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 3
    assert books[-1]['year'] == 2021


def test_delete_book(monkeypatch):
    """Тест удаления книги."""
    monkeypatch.setattr('builtins.input', lambda _: '1')
    delete_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 1
    assert books[0]['id'] == 2


def test_delete_book_no_books():
    """Тест удаления книги, если файл пустой."""
    write_file([], filename=TEST_FILE)
    delete_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 0


def test_delete_book_not_found(monkeypatch):
    """Тест удаления книги, если указанного ID нет."""
    monkeypatch.setattr('builtins.input', lambda _: '3')
    delete_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert len(books) == 2


def test_find_books(monkeypatch, capsys):
    """Тест поиска книг."""
    monkeypatch.setattr('builtins.input', lambda _: '1')
    find_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert "Книга 1" in captured.out


def test_find_books_no_matches(monkeypatch, capsys):
    """Тест поиска книг, если совпадений нет."""
    inputs = iter(['1', 'Книга 3'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    find_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Совпадений не найдено.' in captured.out


def test_find_books_empty_file(capsys):
    """Тест поиска книг в пустом файле."""
    write_file([], filename=TEST_FILE)
    find_books(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Нет данных для поиска.' in captured.out
    assert len(books) == 0


def test_update_book(monkeypatch):
    """Тест изменения статуса книги."""
    inputs = iter(['1', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    update_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    assert books[0]['status'] is False


def test_update_book_invalid_id(monkeypatch, capsys):
    """Тест обновления книги с некорректным ID."""
    inputs = iter(['-1', '1', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    update_book(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'id книги должен быть положительным целым числом.' in captured.out


def test_update_book_not_found(monkeypatch, capsys):
    """Тест обновления книги, если указанного ID нет."""
    monkeypatch.setattr('builtins.input', lambda _: '3')
    update_book(filename=TEST_FILE)
    books = read_file(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Книга с id 3 не найдена.' in captured.out


def test_list_books(capsys):
    """Тест отображения всех книг."""
    list_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert "Книга 1" in captured.out
    assert "Книга 2" in captured.out


def test_list_books_empty_file(capsys):
    """Тест отображения всех книг в пустом файле."""
    write_file([], filename=TEST_FILE)
    list_books(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Нет данных для вывода.' in captured.out
