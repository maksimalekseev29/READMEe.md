"""Test Driver для HabitModule. Запуск: python test_menu.py"""
from menu import HabitModule, HabitError

passed = failed = 0


def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name}")


def raises(f, exc=HabitError):
    try:
        f()
    except exc:
        return True
    except Exception:
        return False
    return False


def names(lst):
    return [h["name"] for h in lst]


def habit(**kw):
    base = {"id": 1, "name": "X", "category": "спорт", "periodicity": "daily", "target_time": "10:00", "available": True}
    base.update(kw)
    return base


def run_tests():
    m = HabitModule()

    # --- Позитивные ---
    check("T1 все привычки", len(m.get_filtered_habits()) == 6)
    check("T2 категория 'спорт'", names(m.get_filtered_habits("спорт")) == ["Зарядка", "Бег"])
    check("T3 спорт + только активные", names(m.get_filtered_habits("спорт", True)) == ["Зарядка", "Бег"])
    check("T4 только активные, без категории",
          "Медитация" not in names(m.get_filtered_habits(only_available=True)))
    check("T5 пустой список -> []", HabitModule([]).get_filtered_habits() == [])
    check("T6 категория без привычек -> []", m.get_filtered_habits("работа") == [])

    # --- Негативные (стресс-тест) ---
    check("N1 'Спорт' в другом регистре", len(m.get_filtered_habits("Спорт")) == 2)
    check("N2 ' спорт ' с пробелами", len(m.get_filtered_habits(" спорт ")) == 2)
    check("N3 неизвестная категория -> ошибка", raises(lambda: m.get_filtered_habits("финансы")))
    check("N4 category=123 -> ошибка", raises(lambda: m.get_filtered_habits(123)))
    check("N5 category='а'*10000 -> ошибка", raises(lambda: m.get_filtered_habits("а" * 10000)))
    check("N6 only_available='нет' -> ошибка", raises(lambda: m.get_filtered_habits("спорт", "нет")))
    r = m.get_filtered_habits("спорт")
    r[0]["target_time"] = "99:99"
    check("N7 мутация результата не портит данные", m.get_filtered_habits("спорт")[0]["target_time"] == "07:30")
    check("N8 время '25:00' при создании -> ошибка", raises(lambda: HabitModule([habit(target_time="25:00")])))
    check("N9 привычка без полей -> HabitError, не KeyError",
          raises(lambda: HabitModule([{"id": 1, "name": "X"}])))
    check("N10 habits не список -> ошибка", raises(lambda: HabitModule("вода")))
    check("N11 время NaN -> ошибка", raises(lambda: HabitModule([habit(target_time=float("nan"))])))
    check("N12 время inf -> ошибка", raises(lambda: HabitModule([habit(target_time=float("inf"))])))
    check("N13 дубликат id -> ошибка",
          raises(lambda: HabitModule([habit(id=1), habit(id=1, name="Y")])))
    check("N14 category='' -> ошибка", raises(lambda: m.get_filtered_habits("")))

    print(f"\nИтого: {passed} PASS, {failed} FAIL")
    assert failed == 0


if __name__ == "__main__":
    run_tests()
