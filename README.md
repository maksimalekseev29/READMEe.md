# Лабораторная работа №3 —

**Интерфейс:** `get_filtered_menu(category, only_available)`

## Файлы

| Файл | Назначение |
| --- | --- |
| `menu.py` | Модуль `MenuModule` (итоговая версия с валидацией) |
| `test_menu.py` | Test Driver: 6 позитивных и 14 негативных тестов |
| `menu_naive.py` | Первая версия без валидации — только для воспроизведения багов |
| `demo_bugs.py` | Запускает наивную версию и печатает фактические результаты для Bug Report |
| `report_lab3.md` | Отчёт: архитектура, интерфейс, тесты, Bug Report, канбан |

## Запуск

```bash
python test_menu.py   # ожидается: 20 PASS, 0 FAIL
python demo_bugs.py   # воспроизведение багов на наивной версии
```

Требуется Python 3.8+, внешние библиотеки не нужны.

## Пример

```python
from menu import MenuModule

m = MenuModule()
m.get_filtered_menu("суп", only_available=True)   # [{'id': 1, 'name': 'Борщ', ...}]
m.get_filtered_menu("пицца")                      # MenuError: неизвестная категория
```

