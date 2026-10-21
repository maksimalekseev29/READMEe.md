"""ПЕРВАЯ (наивная) версия HabitModule — без валидации.
Нужна только для воспроизведения багов (см. demo_bugs.py и report_lab3.md).
"""


class HabitModuleNaive:
    def __init__(self, habits=None):
        if habits is None:
            habits = [
                {"id": 1, "name": "Пить воду", "category": "здоровье", "periodicity": "daily", "target_time": "09:00", "available": True},
                {"id": 2, "name": "Медитация", "category": "здоровье", "periodicity": "daily", "target_time": "08:00", "available": False},
                {"id": 3, "name": "Зарядка", "category": "спорт", "periodicity": "daily", "target_time": "07:30", "available": True},
                {"id": 4, "name": "Бег", "category": "спорт", "periodicity": "weekly", "target_time": "18:00", "available": True},
                {"id": 5, "name": "Чтение книги", "category": "развитие", "periodicity": "daily", "target_time": "21:00", "available": True},
                {"id": 6, "name": "Уборка", "category": "быт", "periodicity": "weekly", "target_time": "12:00", "available": True},
            ]
        self._habits = habits

    def get_filtered_habits(self, category=None, only_available=False):
        result = []
        for h in self._habits:
            if category is not None and h["category"] != category:
                continue
            if only_available and not h["available"]:
                continue
            result.append(h)
        return result
