"""Вспомогательные функции безопасного ввода данных."""


def input_int(prompt: str, minimum: int = 1) -> int:
    """
    Запрашивает у пользователя целое число и возвращает его.

    Число не должно быть меньше minimum (по умолчанию больше нуля).
    При некорректном вводе печатает сообщение об ошибке и повторяет
    запрос.
    """
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                raise ValueError(
                    f"Число должно быть не меньше {minimum}"
                )
            return value
        except ValueError as error:
            print(f"Ошибка ввода: {error}. Попробуйте снова.")


def input_name(prompt: str, fallback: str = "") -> str:
    """
    Запрашивает у пользователя строку и убирает пробелы по краям.

    Если введена пустая строка, возвращает fallback
    (значение по умолчанию).
    """
    name = input(prompt).strip()
    return name if name else fallback
