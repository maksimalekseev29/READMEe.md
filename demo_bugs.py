"""Воспроизведение багов на наивной версии (menu_naive.py).
Запуск: python demo_bugs.py — выводит ФАКТИЧЕСКИЕ результаты для Bug Report.
"""
from menu_naive import MenuModule


def show(bug, title, f):
    try:
        print(f"{bug} | {title} -> {f()!r}")
    except Exception as e:
        print(f"{bug} | {title} -> ИСКЛЮЧЕНИЕ {type(e).__name__}: {e}")


m = MenuModule()
show("BUG-01", "category='пицца'", lambda: m.get_filtered_menu("пицца"))
show("BUG-02", "category='Суп'", lambda: len(m.get_filtered_menu("Суп")))
show("BUG-02", "category=' суп '", lambda: len(m.get_filtered_menu(" суп ")))
show("BUG-03", "category=123", lambda: m.get_filtered_menu(123))
show("BUG-04", "only_available='нет' (Солянка в результате?)",
     lambda: [d["name"] for d in m.get_filtered_menu("суп", "нет")])


m2 = MenuModule()
r = m2.get_filtered_menu("суп")
r[0]["price"] = -999
show("BUG-05", "r[0]['price'] = -999, затем повторный запрос",
     lambda: m2.get_filtered_menu("суп")[0]["price"])
show("BUG-06a", "цена -50 при создании",
     lambda: MenuModule([{"id": 1, "name": "X", "category": "суп", "price": -50, "available": True}])
     and "принято без ошибки")
show("BUG-06b", "блюдо без поля category, фильтр 'суп'",
     lambda: MenuModule([{"id": 1, "name": "X"}]).get_filtered_menu("суп"))
show("BUG-07", "category='а'*10000", lambda: m.get_filtered_menu("а" * 10000))
show("BUG-08", "цена NaN при создании",
     lambda: MenuModule([{"id": 1, "name": "X", "category": "суп", "price": float("nan"), "available": True}])
     and "принято без ошибки")
show("BUG-09", "два блюда с одинаковым id",
     lambda: len(MenuModule([
         {"id": 1, "name": "X", "category": "суп", "price": 1, "available": True},
         {"id": 1, "name": "Y", "category": "суп", "price": 2, "available": True}]).get_filtered_menu()))
