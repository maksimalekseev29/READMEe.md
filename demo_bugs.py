"""Воспроизведение багов на наивной версии (menu_naive.py).
Запуск: python demo_bugs.py — выводит ФАКТИЧЕСКИЕ результаты для Bug Report.
"""
from menu_naive import HabitModuleNaive


def show(bug, title, f):
    try:
        print(f"{bug} | {title} -> {f()!r}")
    except Exception as e:
        print(f"{bug} | {title} -> ИСКЛЮЧЕНИЕ {type(e).__name__}: {e}")


m = HabitModuleNaive()

# --- Баги, связанные с категориями и регистром ---
show("BUG-01", "category='спорт'", lambda: m.get_filtered_habits("спорт"))
show("BUG-02", "category='Спорт' (верхний регистр)", lambda: len(m.get_filtered_habits("Спорт")))
show("BUG-02", "category=' спорт ' (пробелы)", lambda: len(m.get_filtered_habits(" спорт ")))

# --- Баг с неверным типом данных ---
show("BUG-03", "category=123 (число вместо строки)", lambda: m.get_filtered_habits(123))

# --- Баг с неверным флагом доступности ---
show("BUG-04", "only_available='нет' (строка вместо bool). Возвращает ли скрытые привычки?",
     lambda: [h["name"] for h in m.get_filtered_habits("здоровье", "нет")])

# --- Баг с мутацией внутренних данных (изменение через результат) ---
m2 = HabitModuleNaive()
r = m2.get_filtered_habits("здоровье")
if r:
    r[0]["target_time"] = "99:99"  # Ломаем время
show("BUG-05", "r[0]['target_time'] = '99:99', затем повторный запрос",
     lambda: m2.get_filtered_habits("здоровье")[0]["target_time"])

# --- Баги при создании/инициализации ---
show("BUG-06a", "периодичность 'every_day' (невалидная) при создании",
     lambda: HabitModuleNaive([{"id": 1, "name": "X", "category": "спорт", "periodicity": "every_day", "available": True}])
     and "принято без ошибки")

show("BUG-06b", "привычка без поля category, фильтр 'спорт'",
     lambda: HabitModuleNaive([{"id": 1, "name": "X"}]).get_filtered_habits("спорт"))

# --- Стресс-тест на длинную строку ---
show("BUG-07", "category='а'*10000", lambda: m.get_filtered_habits("а" * 10000))

# --- Баг с некорректным ID ---
show("BUG-08", "id = NaN (не число) при создании",
     lambda: HabitModuleNaive([{"id": float("nan"), "name": "X", "category": "спорт", "available": True}])
     and "принято без ошибки")

# --- Баг с дубликатами ID ---
show("BUG-09", "две привычки с одинаковым id",
     lambda: len(HabitModuleNaive([
         {"id": 1, "name": "X", "category": "спорт", "available": True},
         {"id": 1, "name": "Y", "category": "спорт", "available": True}]).get_filtered_habits()))
