import flet as ft


def events_screen():
    return ft.Column(
        [
            ft.Icon(ft.Icons.CALENDAR_MONTH, size=64),
            ft.Text("Events", size=26, weight=ft.FontWeight.BOLD),
            ft.Text("Your schedule will appear here", size=14),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )


def add_event_screen():
    return ft.Column(
        [
            ft.Text("Add Event", size=26, weight=ft.FontWeight.BOLD),
            ft.TextField(label="Title"),
            ft.TextField(label="Date"),
            ft.TextField(label="Time"),
            ft.Dropdown(
                label="Category",
                options=[
                    ft.dropdown.Option("Class"),
                    ft.dropdown.Option("Exam"),
                    ft.dropdown.Option("Activity"),
                ],
            ),
            ft.FilledButton("Save", expand=True),
        ],
        spacing=15,
    )


def settings_screen():
    return ft.Column(
        [
            ft.Icon(ft.Icons.SETTINGS, size=64),
            ft.Text("Settings", size=26, weight=ft.FontWeight.BOLD),
            ft.ListTile(title=ft.Text("Sync status"), trailing=ft.Text("Offline")),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
    )


SCREENS = [events_screen, add_event_screen, settings_screen]


def main(page: ft.Page):
    page.title = "Schedule Management System"
    page.padding = 20

    content = ft.Container(expand=True)

    def switch(e):
        content.content = SCREENS[nav.selected_index]()
        page.update()

    nav = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.EVENT_OUTLINED,
                selected_icon=ft.Icons.EVENT,
                label="Events",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                selected_icon=ft.Icons.ADD_CIRCLE,
                label="Add",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
        ],
        on_change=switch,
    )

    page.navigation_bar = nav
    content.content = events_screen()
    page.add(content)


if __name__ == "__main__":
    ft.run(main)
