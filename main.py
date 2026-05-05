import flet as ft
def main(page: ft.Page):
    page.title = "Income Tracker"
    page.window.width = 400
    page.window.height = 600
    page.window.resizable = False

    operations = []

    operation_list = ft.ListView(expand=True)

    balance_text = ft.Text("Total Balance: $ 0.00", size=16, weight=ft.FontWeight.BOLD)

    def add_operation_dialog(e):

        def close_dialog(e):
            dialog.open = False
            page.update()
        def save_operation(e):
            description = description_field.value
            amount = amount_field.value

            if description and amount:
                try:
                    amount = float(amount)
                    operations.append({"description": description, "amount": amount})

                    operation_list.controls.append(
                        ft.Text(f"{description}: $ {amount:.2f}")
                    )
                    total = sum(
                        item["amount"]
                        for item in operations
                    )
                    balance_text.value = (
                        f"Total Balance: $ {total:.2f}"
                    )

                    dialog.open = False
                    page.update()

                except ValueError as ex:
                    print(f"Error: {ex}")

        description_field = ft.TextField(label = "Description")
        amount_field = ft.TextField(label="Amount", keyboard_type=ft.KeyboardType.NUMBER)

        dialog = ft.AlertDialog(
            title=ft.Text("Add New Operation"),
            content=ft.Column([
                description_field,
                amount_field
            ], tight=True),
            actions=[
                ft.TextButton("Save", on_click=save_operation),
                ft.TextButton("Cancel", on_click=close_dialog)
            ]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT

        page.update()


    def show_statistics(e):
        def close_stat_dialog(e):
            stats_dialog.open = False
            page.update()
        total_income = sum(item["amount"] for item in operations if item["amount"] > 0)
        total_expenses = sum(item["amount"] for item in operations if item["amount"] < 0)

        stats_dialog = ft.AlertDialog(
            title=ft.Text('Statistics'),
            content=ft.Column([
                ft.Text(f"Total income: $ {total_income:.2f}"),
                ft.Text(f"Total expenses: $ {total_expenses:.2f}"),
                ft.Text(f"Net balance: $ {total_income + total_expenses:.2f}")
            ], tight=True),
            actions=[
                ft.TextButton("Close", on_click=close_stat_dialog)
            ]
        )
        page.overlay.append(stats_dialog)
        stats_dialog.open = True
        page.update()


    add_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        on_click=add_operation_dialog
    )

    settings_button = ft.IconButton(
        icon=ft.Icons.SETTINGS,
        tooltip="Settings",
        on_click=toggle_theme
    )

    stats_button = ft.IconButton(
        icon=ft.Icons.INSERT_CHART,
        tooltip="View Statistics",
        on_click=show_statistics
    )

    page.add(
        ft.Column([
            ft.Row([
                ft.Text("Recent Operations", size=20, weight=ft.FontWeight.BOLD),
                settings_button,
                stats_button
            ]),
            balance_text,
            operation_list
        ], expand=True),
        add_button
    )

if __name__ == "__main__":
    ft.run(main)