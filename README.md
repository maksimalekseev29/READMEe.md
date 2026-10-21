 # foodcampus-menu-module
Лабораторная работа №3 — модуль MenuModule проекта «FoodCampus».

История пользователя: Как повар, я хочу фильтровать блюда по категориям, чтобы выдавать актуальное меню. Интерфейс: get_filtered_menu(category, only_available)

Файлы
бер	(
menu.py	Модуль MenuModule(итоговая версия с валидацией)
test_menu.py	Тест-драйвер: 6 положительных и 14 отрицательных тестов
menu_naive.py	Первая версия без валидации — только для ключей багов
demo_bugs.py	Запускает наивную версию и выводит фактические результаты для отчета об ошибках.
report_lab3.md	Отчёт: архитектура, интерфейс, тесты, отчет об ошибках, канбан.
Запуск
python test_menu.py   # ожидается: 20 PASS, 0 FAIL
python demo_bugs.py   # воспроизведение багов на наивной версии
Требуется Python 3.8+, внешние библиотеки не нужны.

ль
from menu import MenuModule

m = MenuModule()
m.get_filtered_menu("суп", only_available=True)   # [{'id': 1, 'name': 'Борщ', ...}]
m.get_filtered_menu("пицца")                      # MenuError: неизвестная категория

