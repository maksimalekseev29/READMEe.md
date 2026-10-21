"""HabitModule — модуль привычек проекта HabitTracker.

User Story: Как пользователь, я хочу фильтровать свои привычки по категориям,
чтобы видеть только нужные мне в данный момент.
Интерфейс: get_filtered_habits(category, only_available)
"""
import math

CATEGORIES = ("здоровье", "спорт", "развитие", "работа", "быт")
PERIODICITY_TYPES = ("daily", "weekly")
MAX_CATEGORY_LEN = 50


class HabitError(ValueError):
    """Ошибка входных данных модуля привычек."""


class StreakStub:
    """Заглушка (Stub) модуля стриков: всегда отвечает, что серия активна."""

    def is_streak_active(self, habit_id):
        return True


def _default_habits():
    return [
        {"id": 1, "name": "Пить воду", "category": "здоровье", "periodicity": "daily", "target_time": "09:00", "available": True},
        {"id": 2, "name": "Медитация", "category": "здоровье", "periodicity": "daily", "target_time": "08:00", "available": False},
        {"id": 3, "name": "Зарядка", "category": "спорт", "periodicity": "daily", "target_time": "07:30", "available": True},
        {"id": 4, "name": "Бег", "category": "спорт", "periodicity": "weekly", "target_time": "18:00", "available": True},
        {"id": 5, "name": "Чтение книги", "category": "развитие", "periodicity": "daily", "target_time": "21:00", "available": True},
        {"id": 6, "name": "Уборка", "category": "быт", "periodicity": "weekly", "target_time": "12:00", "available": True},
    ]


def _validate_habit(h):
    if not isinstance(h, dict):
        raise HabitError("Привычка должна быть словарём")
    for key in ("id", "name", "category", "periodicity", "target_time", "available"):
        if key not in h:
            raise HabitError(f"У привычки нет поля '{key}'")
            
    if not isinstance(h["name"], str) or not h["name"].strip():
        raise HabitError("Название привычки должно быть непустой строкой")
        
    if h["category"] not in CATEGORIES:
        raise HabitError(f"Неизвестная категория привычки: {h['category']!r}")
        
    if h["periodicity"] not in PERIODICITY_TYPES:
        raise HabitError(f"Неверная периодичность: {h['periodicity']!r}. Допустимо: {', '.join(PERIODICITY_TYPES)}")
        
    # Валидация target_time (время в формате HH:MM)
    target_time = h["target_time"]
    if not isinstance(target_time, str):
        raise HabitError("Время выполнения должно быть строкой")
    try:
        hours, minutes = map(int, target_time.split(":"))
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError
    except (ValueError, AttributeError):
        raise HabitError("Время выполнения должно быть в формате 'HH:MM'")
        
    if not isinstance(h["available"], bool):
        raise HabitError("Поле 'available' должно быть bool")


class HabitModule:
    def __init__(self, habits=None, streak_service=None):
        habits = _default_habits() if habits is None else habits
        if not isinstance(habits, list):
            raise HabitError("Список привычек должен быть list")
            
        seen_ids = set()
        for h in habits:
            _validate_habit(h)
            if h["id"] in seen_ids:
                raise HabitError(f"Повторяющийся id привычки: {h['id']!r}")
            seen_ids.add(h["id"])
            
        self._habits = [dict(h) for h in habits]
        self._streak_service = streak_service if streak_service is not None else StreakStub()

    def get_filtered_habits(self, category=None, only_available=False):
        """Вернуть список привычек (копии), отфильтрованных по категории и наличию.

        category: None (все) или одна из CATEGORIES (регистр и пробелы игнорируются).
        only_available: bool.
        Raises HabitError при неверных аргументах.
        """
        if category is not None:
            if not isinstance(category, str):
                raise HabitError("category должна быть строкой или None")
            if len(category) > MAX_CATEGORY_LEN:
                raise HabitError("category слишком длинная")
            category = category.strip().lower()
            if category not in CATEGORIES:
                raise HabitError(
                    f"Неизвестная категория: {category!r}. Допустимо: {', '.join(CATEGORIES)}"
                )
                
        if not isinstance(only_available, bool):
            raise HabitError("only_available должен быть bool")

        result = []
        for h in self._habits:
            if category is not None and h["category"] != category:
                continue
            if only_available and not (h["available"] and self._streak_service.is_streak_active(h["id"])):
                continue
            result.append(dict(h))
        return result
