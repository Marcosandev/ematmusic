import flet as ft

def AppHeader(page: ft.Page, title: str | None = None) -> ft.Container:
    """Return a small header container with app title aligned to top-left.

    By default the header uses a fixed application name so it does not depend
    on `page.title`. If an explicit `title` is provided it will be used.
    """
    if not title:
        title = "EMATMUS♪C"
    return ft.Container(
        content=ft.Row([
            ft.Text(title, weight=ft.FontWeight.BOLD, size=20, color=ft.Colors.BLUE),
        ]),
        padding=ft.Padding.only(left=16, top=8, bottom=4),
    )
