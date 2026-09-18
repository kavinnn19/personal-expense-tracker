import expense_manager


def setup_test_csv(tmp_path, monkeypatch):
    test_file = tmp_path / "test_expenses.csv"

    monkeypatch.setattr(
        expense_manager,
        "CSV_FILE",
        str(test_file)
    )

    expense_manager.initialize_csv()


def test_add_expense(tmp_path, monkeypatch):
    setup_test_csv(tmp_path, monkeypatch)

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Lunch",
        150
    )

    expenses = expense_manager.get_expenses()

    assert len(expenses) == 1
    assert expenses[0]["category"] == "Food"
    assert expenses[0]["description"] == "Lunch"
    assert float(expenses[0]["amount"]) == 150


def test_search_expenses(tmp_path, monkeypatch):
    setup_test_csv(tmp_path, monkeypatch)

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Lunch",
        150
    )

    expense_manager.add_expense(
        "2026-09-18",
        "Transport",
        "Bus",
        50
    )

    results = expense_manager.search_expenses("lunch")

    assert len(results) == 1
    assert results[0]["description"] == "Lunch"


def test_delete_expense(tmp_path, monkeypatch):
    setup_test_csv(tmp_path, monkeypatch)

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Lunch",
        150
    )

    deleted = expense_manager.delete_expense(1)

    assert deleted is True

    expenses = expense_manager.get_expenses()

    assert len(expenses) == 0


def test_calculate_total(tmp_path, monkeypatch):
    setup_test_csv(tmp_path, monkeypatch)

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Lunch",
        150
    )

    expense_manager.add_expense(
        "2026-09-18",
        "Transport",
        "Bus",
        50
    )

    total = expense_manager.calculate_total()

    assert total == 200


def test_category_totals(tmp_path, monkeypatch):
    setup_test_csv(tmp_path, monkeypatch)

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Lunch",
        150
    )

    expense_manager.add_expense(
        "2026-09-18",
        "Food",
        "Dinner",
        250
    )

    expense_manager.add_expense(
        "2026-09-18",
        "Transport",
        "Bus",
        50
    )

    totals = expense_manager.calculate_category_totals()

    assert totals["Food"] == 400
    assert totals["Transport"] == 50