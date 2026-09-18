import streamlit as st
from datetime import date

from expense_manager import (
    initialize_csv,
    add_expense,
    get_expenses,
    search_expenses,
    filter_by_category,
    filter_by_date,
    delete_expense,
    calculate_total,
    calculate_category_totals
)


# Create CSV file if it does not exist
initialize_csv()


# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# Title
st.title("💰 Personal Expense Tracker")
st.write("Track, search, filter and manage your daily expenses.")


# Sidebar
st.sidebar.header("Menu")

menu = st.sidebar.radio(
    "Choose an option:",
    [
        "Add Expense",
        "View Expenses",
        "Search & Filter",
        "Delete Expense",
        "Summary"
    ]
)


# --------------------------------------------------
# ADD EXPENSE
# --------------------------------------------------

if menu == "Add Expense":

    st.header("➕ Add Expense")

    expense_date = st.date_input(
        "Date",
        value=date.today()
    )

    category = st.selectbox(
        "Category",
        [
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Entertainment",
            "Health",
            "Education",
            "Other"
        ]
    )

    description = st.text_input(
        "Description",
        placeholder="Example: Lunch"
    )

    amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0
    )

    if st.button("Add Expense"):

        if description.strip() == "":
            st.error("Please enter a description.")

        elif amount <= 0:
            st.error("Amount must be greater than 0.")

        else:
            add_expense(
                str(expense_date),
                category,
                description,
                amount
            )

            st.success("Expense added successfully!")


# --------------------------------------------------
# VIEW EXPENSES
# --------------------------------------------------

elif menu == "View Expenses":

    st.header("📋 All Expenses")

    expenses = get_expenses()

    if expenses:

        st.dataframe(
            expenses,
            use_container_width=True
        )

    else:
        st.info("No expenses found.")


# --------------------------------------------------
# SEARCH AND FILTER
# --------------------------------------------------

elif menu == "Search & Filter":

    st.header("🔍 Search & Filter Expenses")

    search_type = st.radio(
        "Choose filter:",
        [
            "Search keyword",
            "Filter by category",
            "Filter by date"
        ]
    )

    if search_type == "Search keyword":

        keyword = st.text_input(
            "Enter description or category"
        )

        if keyword:

            results = search_expenses(keyword)

            if results:
                st.dataframe(
                    results,
                    use_container_width=True
                )
            else:
                st.warning("No matching expenses found.")

    elif search_type == "Filter by category":

        category = st.selectbox(
            "Select category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Health",
                "Education",
                "Other"
            ]
        )

        results = filter_by_category(category)

        if results:
            st.dataframe(
                results,
                use_container_width=True
            )
        else:
            st.warning("No expenses found for this category.")

    else:

        selected_date = st.date_input(
            "Select date"
        )

        results = filter_by_date(
            str(selected_date)
        )

        if results:
            st.dataframe(
                results,
                use_container_width=True
            )
        else:
            st.warning("No expenses found for this date.")


# --------------------------------------------------
# DELETE EXPENSE
# --------------------------------------------------

elif menu == "Delete Expense":

    st.header("🗑️ Delete Expense")

    expenses = get_expenses()

    if expenses:

        expense_ids = [
            int(expense["id"])
            for expense in expenses
        ]

        selected_id = st.selectbox(
            "Select expense ID to delete",
            expense_ids
        )

        if st.button("Delete Expense"):

            deleted = delete_expense(selected_id)

            if deleted:
                st.success(
                    f"Expense {selected_id} deleted successfully!"
                )

            else:
                st.error("Expense not found.")

    else:
        st.info("There are no expenses to delete.")


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

elif menu == "Summary":

    st.header("📊 Expense Summary")

    total = calculate_total()

    st.metric(
        "💰 Total Spending",
        f"₹{total:.2f}"
    )

    st.subheader("📊 Category-wise Spending")

    category_totals = calculate_category_totals()

    if category_totals:

        for category, amount in category_totals.items():

            st.write(
                f"**{category}:** ₹{amount:.2f}"
            )

    else:
        st.info("No expenses available.")