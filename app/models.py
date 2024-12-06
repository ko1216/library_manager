from app.services import read_file, write_file, FILE_PATH


class Book:
    """
    Класс для представления книги в библиотеке
    """

    def __init__(self, title, author, year, status=True, filename=FILE_PATH) -> None:
        self.filename = filename
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

    def generate_id(self) -> int:
        """
        Генерирует уникальный id для новой книги.
        """
        data = read_file(filename=self.filename, silent=True)
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
        books = read_file(filename=self.filename)
        books.append(self.to_dict())
        write_file(books, filename=self.filename)

    def show_status(self) -> str:
        """
        Возвращает текущий статус книги в виде строки.
        """
        if self.status:
            return 'В наличии'
        else:
            return 'Выдана'
