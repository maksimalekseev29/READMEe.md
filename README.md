 #

Лабораторная работа №3 — Трекер привычек (Карточка 4).
Интерфейс: get_filtered_habits(category, only_available)

# Файлы
menu.py          Модуль HabitModule (итоговая версия с валидацией)
test_menu.py     Тест-драйвер: 6 положительных и 14 отрицательных тестов
menu_naive.py    Первая версия без валидации — только для ключей багов
demo_bugs.py     Запускает наивную версию и выводит фактические результаты для отчета об ошибках.
report_lab3.md   Отчёт: архитектура, интерфейс, тесты, отчет об ошибках, канбан.

# Запуск
python test_menu.py   # ожидается: 20 PASS, 0 FAIL
python demo_bugs.py   # воспроизведение багов на наивной версии
Требуется Python 3.8+, внешние библиотеки не нужны.

# 
from menu import HabitModule

m = HabitModule()
m.get_filtered_habits("здоровье", only_available=True)   # [{'id': 1, 'name': 'Пить воду', ...}]
m.get_filtered_habits("финансы")                         # HabitError: неизвестная категория
