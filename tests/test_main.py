import os
import pytest
from app.main import main
from app.services import read_file, write_file

TEST_FILE = 'test_books.json'


@pytest.fixture(autouse=True)
def setup_mock_file():
    """Создаёт тестовые данные для main.py."""
    sample_data = [
        {'id': 1, 'title': 'Книга 1', 'author': 'Автор 1', 'year': 2020, 'status': True},
        {'id': 2, 'title': 'Книга 2', 'author': 'Автор 2', 'year': 2019, 'status': False},
    ]
    write_file(sample_data, filename=TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_main_add_book(monkeypatch, capsys):
    """Тест выбора пункта меню 'Добавить книгу'."""
    inputs = iter(['1', 'Новая Книга', 'Автор 3', '2022', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Книга "Новая Книга" успешно добавлена.' in captured.out
    books = read_file(filename=TEST_FILE)
    assert len(books) == 3
    assert books[-1]['title'] == 'Новая Книга'


def test_main_delete_book(monkeypatch, capsys):
    """Тест выбора пункта меню 'Удалить книгу'."""
    inputs = iter(['2', '1', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Книга с id 1 успешно удалена.' in captured.out
    books = read_file(filename=TEST_FILE)
    assert len(books) == 1


def test_main_find_books(monkeypatch, capsys):
    """Тест выбора пункта меню 'Найти книги'."""
    inputs = iter(['3', '1', 'Книга 1', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Найдено совпадений: 1' in captured.out
    assert 'Книга 1' in captured.out


def test_main_update_book(monkeypatch, capsys):
    """Тест выбора пункта меню 'Изменить статус книги'."""
    inputs = iter(['4', '2', '1', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Статус книги с id 2 успешно обновлён.' in captured.out
    books = read_file(filename=TEST_FILE)
    assert books[1]['status'] is True


def test_main_list_books(monkeypatch, capsys):
    """Тест выбора пункта меню 'Показать все книги'."""
    inputs = iter(['5', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Список всех книг:' in captured.out
    assert 'Книга 1' in captured.out
    assert 'Книга 2' in captured.out


def test_main_invalid_choice(monkeypatch, capsys):
    """Тест ввода некорректного пункта меню."""
    inputs = iter(['0', '', '6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Некорректный ввод. Пожалуйста, выберите номер из списка.' in captured.out


def test_main_exit(monkeypatch, capsys):
    """Тест выхода из программы."""
    inputs = iter(['6'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main(filename=TEST_FILE)
    captured = capsys.readouterr()
    assert 'Спасибо за использование библиотеки! До свидания!' in captured.out
