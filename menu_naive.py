"""ПЕРВАЯ (наивная) версия MenuModule — без валидации.
Нужна только для воспроизведения багов (см. demo_bugs.py и report_lab3.md).
"""


class MenuModule:
    def __init__(self, dishes=None):
        if dishes is None:
            dishes = [
                {"id": 1, "name": "Борщ", "category": "суп", "price": 120, "available": True},
                {"id": 2, "name": "Солянка", "category": "суп", "price": 140, "available": False},
                {"id": 3, "name": "Котлета с пюре", "category": "второе", "price": 180, "available": True},
                {"id": 4, "name": "Греча с курицей", "category": "второе", "price": 160, "available": True},
                {"id": 5, "name": "Цезарь", "category": "салат", "price": 150, "available": True},
                {"id": 6, "name": "Компот", "category": "напиток", "price": 40, "available": True},
            ]
        self._dishes = dishes

    def get_filtered_menu(self, category=None, only_available=False):
        result = []
        for d in self._dishes:
            if category is not None and d["category"] != category:
                continue
            if only_available and not d["available"]:
                continue
            result.append(d)
        return result
