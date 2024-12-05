from models import Book, read_file, write_file


def create_book():
    """
    Функция создания новой книги с указанными полями.
    """
    while True:
        title_input = str(input('Введите название книги: '))
        if title_input.strip():
            break
        else:
            print('Название книги не может быть пустым.')
    while True:
        author_input = str(input('Введите ФИО автора: '))
        if author_input.strip():
            break
        else:
            print('ФИО автора не может быть пустым.')
    while True:
        year_input = input('Введите год написания книги: ')
        if year_input.strip() and year_input.isdigit():
            year_input = int(year_input)
            break
        else:
            print('Год написания книги должен быть целым числом и не пустым.')
    try:
        book = Book(title_input, author_input, year_input)
        print(f'Книга "{book.title}" успешно добавлена.')
    except Exception as e:
        print(f'Ошибка при создании книги: {e}')


def delete_book():
    """
    Функция удаления книги по id.
    """
    try:
        books = read_file()
        if not books:
            print('Нет данных для удаления.')
            return

        book_id = input('Введите id книги для удаления: ').strip()
        while not book_id.isdigit() or int(book_id) <= 0:
            print('id книги должен быть положительным целым числом.')
            book_id = input('Введите id книги для удаления: ').strip()
        book_id = int(book_id)

        book_found = False
        for book in books:
            if book['id'] == book_id:
                books.remove(book)
                book_found = True
                break

        if not book_found:
            print(f'Книга с id {book_id} не найдена.')
            return

        write_file(books)
        print(f'Книга с id {book_id} успешно удалена.')
    except Exception as e:
        print(f'Ошибка при удалении книги: {e}')


def find_books():
    """
    Функция поиска книг/и по названию, автору или году.
    """
    books = read_file()
    if not books:
        print('Нет данных для поиска.')
        return

    print('По какому критерию выполнить поиск?\n'
          '1. Название\n'
          '2. Автор\n'
          '3. Год написания')

    variant = input('Выберите вариант (1, 2 или 3): ').strip()
    while variant not in ['1', '2', '3']:
        print('Введите корректное значение (1, 2 или 3).')
        variant = input('Выберите вариант (1, 2 или 3): ').strip()

    query = input('Введите значение для поиска: ').strip()
    while not query:
        print('Значение для поиска не может быть пустым.')

    matches = []
    if variant == '1':
        matches = [book for book in books if query.lower() in book['title'].lower()]
    elif variant == '2':
        matches = [book for book in books if query.lower() in book['author'].lower()]
    elif variant == '3':
        if query.isdigit():
            matches = [book for book in books if book['year'] == int(query)]
        else:
            print('Год должен быть числом.')
            return

    if matches:
        print(f'Найдено совпадений: {len(matches)}')
        for book in matches:
            print(f'id: {book['id']},\n'
                  f'Название: {book['title']},\n'
                  f'Автор: {book['author']},\n'
                  f'Год написания: {book['year']},\n'
                  f'Статус: {'В наличии' if book['status'] else 'Выдана'}')
    else:
        print('Совпадений не найдено.')


def update_book():
    """
    Функция для изменения статуса книги по id.
    """
    books = read_file()
    if not books:
        print('Нет данных для обновления.')
        return

    book_id = input('Введите id книги для изменения статуса: ').strip()
    while not book_id.isdigit() or int(book_id) <= 0:
        print('id книги должен быть положительным целым числом.')
        book_id = input('Введите id книги для изменения статуса: ').strip()
    book_id = int(book_id)

    book_found = False
    for book in books:
        if book['id'] == book_id:
            book_found = True
            print(f'Текущий статус книги "{book['title']}": {'В наличии' if book['status'] else 'Выдана'}')
            new_status = input('Введите новый статус (1 - В наличии, 0 - Выдана): ').strip()
            while new_status not in {'0', '1'}:
                print('Введите корректное значение: 1 - В наличии, 0 - Выдана.')
                new_status = input('Введите новый статус (1 - В наличии, 0 - Выдана): ').strip()
            book['status'] = new_status == '1'
            print(f'Статус книги с id {book_id} успешно обновлён.')
            break

    if not book_found:
        print(f'Книга с id {book_id} не найдена.')
        return

    write_file(books)


def list_books():
    """
    Функция вывода списка всех книг.
    """
    books = read_file()
    if not books:
        print('Нет данных для вывода.')
        return

    print(f'Всего книг: {len(books)}\nСписок всех книг:')
    for book in books:
        print(f'\nid: {book['id']},\n'
              f'Название: {book['title']},\n'
              f'Автор: {book['author']},\n'
              f'Год написания: {book['year']},\n'
              f'Статус: {'В наличии' if book['status'] else 'Выдана'}.')
