"""Test Driver для MenuModule. Запуск: python test_menu.py"""
from menu import MenuModule, MenuError

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name}")


def raises(f, exc=MenuError):
    try:
        f()
    except exc:
        return True
    except Exception:
        return False
    return False


def names(lst):
    return [d["name"] for d in lst]


def dish(**kw):
    base = {"id": 1, "name": "X", "category": "суп", "price": 10, "available": True}
    base.update(kw)
    return base


def run_tests():
    m = MenuModule()

    # --- Позитивные ---
    check("T1 все блюда", len(m.get_filtered_menu()) == 6)
    check("T2 категория 'суп'", names(m.get_filtered_menu("суп")) == ["Борщ", "Солянка"])
    check("T3 суп + только в наличии", names(m.get_filtered_menu("суп", True)) == ["Борщ"])
    check("T4 только в наличии, без категории",
          "Солянка" not in names(m.get_filtered_menu(only_available=True)))
    check("T5 пустое меню -> []", MenuModule([]).get_filtered_menu() == [])
    check("T6 категория без блюд -> []", m.get_filtered_menu("десерт") == [])

    # --- Негативные (стресс-тест) ---
    check("N1 'Суп' в другом регистре", len(m.get_filtered_menu("Суп")) == 2)
    check("N2 ' суп ' с пробелами", len(m.get_filtered_menu(" суп ")) == 2)
    check("N3 неизвестная категория -> ошибка", raises(lambda: m.get_filtered_menu("пицца")))
    check("N4 category=123 -> ошибка", raises(lambda: m.get_filtered_menu(123)))
    check("N5 category='а'*10000 -> ошибка", raises(lambda: m.get_filtered_menu("а" * 10000)))
    check("N6 only_available='нет' -> ошибка", raises(lambda: m.get_filtered_menu("суп", "нет")))
    r = m.get_filtered_menu("суп")
    r[0]["price"] = -999
    check("N7 мутация результата не портит данные", m.get_filtered_menu("суп")[0]["price"] == 120)
    check("N8 цена -50 при создании -> ошибка", raises(lambda: MenuModule([dish(price=-50)])))
    check("N9 блюдо без полей -> MenuError, не KeyError",
          raises(lambda: MenuModule([{"id": 1, "name": "X"}])))
    check("N10 dishes не список -> ошибка", raises(lambda: MenuModule("борщ")))
    check("N11 цена NaN -> ошибка", raises(lambda: MenuModule([dish(price=float("nan"))])))
    check("N12 цена inf -> ошибка", raises(lambda: MenuModule([dish(price=float("inf"))])))
    check("N13 дубликат id -> ошибка",
          raises(lambda: MenuModule([dish(id=1), dish(id=1, name="Y")])))
    check("N14 category='' -> ошибка", raises(lambda: m.get_filtered_menu("")))

    print(f"\nИтого: {passed} PASS, {failed} FAIL")
    assert failed == 0


if __name__ == "__main__":
    run_tests()
