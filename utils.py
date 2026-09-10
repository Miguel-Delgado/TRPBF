"""Вспомогательные функции безопасного ввода данных."""


def input_int(prompt: str) -> int:
    """
    Запрашивает у пользователя целое число и возвращает его.

    Число должно быть больше 0. При некорректном вводе
    (не целое число или число <= 0) печатает сообщение
    об ошибке и повторяет запрос.
    """
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError("Число должно быть больше 0")
            return value
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Попробуйте снова.")


def input_name(prompt: str, fallback: str = "") -> str:
    """
    Запрашивает у пользователя строку и убирает пробелы по краям.

    Если введена пустая строка, возвращает fallback
    (значение по умолчанию).
    """
    name = input(prompt).strip()
    return name if name else fallback
