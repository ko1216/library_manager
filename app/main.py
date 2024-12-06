from app.services import FILE_PATH
from app.utils import create_book, delete_book, find_books, update_book, list_books
from app.services import FILE_PATH


def main(filename=FILE_PATH):
    """
    Основная функция для управления библиотекой.
    """
    while True:
        print('\nДобро пожаловать в библиотеку!')
        print('Выберите действие:')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Найти книги')
        print('4. Изменить статус книги')
        print('5. Показать все книги')
        print('6. Выйти из программы')

        choice = input('Введите номер действия: ').strip()

        if choice == '1':
            create_book(filename=filename)
        elif choice == '2':
            delete_book(filename=filename)
        elif choice == '3':
            find_books(filename=filename)
        elif choice == '4':
            update_book(filename=filename)
        elif choice == '5':
            list_books(filename=filename)
        elif choice == '6':
            print('Спасибо за использование библиотеки! До свидания!')
            break
        else:
            print('Некорректный ввод. Пожалуйста, выберите номер из списка.')

        input('\nНажмите Enter, чтобы вернуться в главное меню...')


if __name__ == '__main__':
    main()
