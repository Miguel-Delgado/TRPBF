import random

# ----- Функция 1: создание турнира (ввод названия) -----
def create_tournament():
    name = input("Введите название турнира: ").strip()
    return name if name else "Турнир без названия"

# ----- Функция 2: добавление участников (ввод имён) -----
def add_participants():
    while True:
        count_str = input("Введите количество участников (целое число > 0): ")
        if count_str.isdigit():
            count = int(count_str)
            if count > 0:
                break
            else:
                print("Ошибка: количество должно быть больше 0.")
        else:
            print("Ошибка: введите целое число.")

    participants = []
    for i in range(1, count + 1):
        name = input(f"Введите имя участника #{i}: ").strip()
        participants.append(name if name else f"Участник {i}")
    return participants

# ----- Функция 3: проверка чётности и добавление 'bye' -----
def ensure_even_number(participants):
    if len(participants) % 2 != 0:
        participants.append("None_name")
        print("Количество участников нечётное. Добавлен виртуальный участник 'None_name'.")
        return participants, True
    return participants, False

# ----- Функция 4: жеребьёвка (формирование пар) -----
def draw_pairs(participants):
    shuffled = participants[:]          # копируем, чтобы не изменять оригинал
    random.shuffle(shuffled)
    pairs = []
    for i in range(0, len(shuffled), 2):
        pairs.append((shuffled[i], shuffled[i+1]))
    return pairs

# ----- Функция 5: вывод пар на экран -----
def display_pairs(tournament_name, pairs):
    print("\n" + "=" * 50)
    print(f"Пары первого тура турнира '{tournament_name}':")
    for idx, (p1, p2) in enumerate(pairs, start=1):
        if p1 == "None_name":
            print(f"  Пара #{idx}: {p1} vs {p2} -> {p2} проходит автоматически.")
        elif p2 == "None_name":
            print(f"  Пара #{idx}: {p1} vs {p2} -> {p1} проходит автоматически.")
        else:
            print(f"  Пара #{idx}: {p1} vs {p2}")
    print("=" * 50)

# ----- Главный сценарий (последовательный вызов функций) -----
def main():
    print("=" * 50)
    print("   Добро пожаловать в систему организации турниров!")
    print("=" * 50)

    # 1. Создание турнира
    tournament_name = create_tournament()

    # 2. Добавление участников
    participants = add_participants()

    print("\nСписок участников:")
    for i, name in enumerate(participants, 1):
        print(f"  {i}. {name}")

    # 3. Проверка чётности
    participants, was_added = ensure_even_number(participants)

    # 4. Жеребьёвка
    pairs = draw_pairs(participants)

    # 5. Вывод пар
    display_pairs(tournament_name, pairs)

    print("Жеребьёвка завершена. Спасибо за использование!")

if __name__ == "__main__":
    main()
