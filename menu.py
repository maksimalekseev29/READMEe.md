"""MenuModule — модуль меню проекта FoodCampus.

User Story: Как повар, я хочу фильтровать блюда по категориям,
чтобы выдавать актуальное меню.
Интерфейс: get_filtered_menu(category, only_available)
"""
import math

CATEGORIES = ("суп", "второе", "салат", "напиток", "десерт")
MAX_CATEGORY_LEN = 50


class MenuError(ValueError):
    """Ошибка входных данных модуля меню."""


class InventoryStub:
    """Заглушка (Stub) склада: всегда отвечает «в наличии»."""

    def is_in_stock(self, dish_id):
        return True


def _default_dishes():
    return [
        {"id": 1, "name": "Борщ", "category": "суп", "price": 120, "available": True},
        {"id": 2, "name": "Солянка", "category": "суп", "price": 140, "available": False},
        {"id": 3, "name": "Котлета с пюре", "category": "второе", "price": 180, "available": True},
        {"id": 4, "name": "Греча с курицей", "category": "второе", "price": 160, "available": True},
        {"id": 5, "name": "Цезарь", "category": "салат", "price": 150, "available": True},
        {"id": 6, "name": "Компот", "category": "напиток", "price": 40, "available": True},
    ]


def _validate_dish(d):
    if not isinstance(d, dict):
        raise MenuError("Блюдо должно быть словарём")
    for key in ("id", "name", "category", "price", "available"):
        if key not in d:
            raise MenuError(f"У блюда нет поля '{key}'")
    if not isinstance(d["name"], str) or not d["name"].strip():
        raise MenuError("Название блюда должно быть непустой строкой")
    if d["category"] not in CATEGORIES:
        raise MenuError(f"Неизвестная категория блюда: {d['category']!r}")
    price = d["price"]
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        raise MenuError("Цена должна быть числом")
    if math.isnan(price) or math.isinf(price) or price < 0:
        raise MenuError("Цена должна быть конечным числом >= 0")
    if not isinstance(d["available"], bool):
        raise MenuError("Поле 'available' должно быть bool")


class MenuModule:
    def __init__(self, dishes=None, inventory=None):
        dishes = _default_dishes() if dishes is None else dishes
        if not isinstance(dishes, list):
            raise MenuError("Список блюд должен быть list")
        seen_ids = set()
        for d in dishes:
            _validate_dish(d)
            if d["id"] in seen_ids:
                raise MenuError(f"Повторяющийся id блюда: {d['id']!r}")
            seen_ids.add(d["id"])
        self._dishes = [dict(d) for d in dishes]
        self._inventory = inventory if inventory is not None else InventoryStub()

    def get_filtered_menu(self, category=None, only_available=False):
        """Вернуть список блюд (копии), отфильтрованных по категории и наличию.

        category: None (все) или одна из CATEGORIES (регистр и пробелы игнорируются).
        only_available: bool.
        Raises MenuError при неверных аргументах.
        """
        if category is not None:
            if not isinstance(category, str):
                raise MenuError("category должна быть строкой или None")
            if len(category) > MAX_CATEGORY_LEN:
                raise MenuError("category слишком длинная")
            category = category.strip().lower()
            if category not in CATEGORIES:
                raise MenuError(
                    f"Неизвестная категория: {category!r}. Допустимо: {', '.join(CATEGORIES)}"
                )
        if not isinstance(only_available, bool):
            raise MenuError("only_available должен быть bool")

        result = []
        for d in self._dishes:
            if category is not None and d["category"] != category:
                continue
            if only_available and not (d["available"] and self._inventory.is_in_stock(d["id"])):
                continue
            result.append(dict(d))
        return result
