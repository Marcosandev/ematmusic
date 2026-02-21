import flet as ft

class NavigationBar(ft.NavigationBar):
    def __init__(self, page: ft.Page | None = None, selected_index: int = 1, dark: bool | None = None):
    
        if dark is None and page is not None:
            dark = page.theme_mode == ft.ThemeMode.DARK

        on_change = self._change_view if page is not None else None

        bgcolor = ft.Colors.BLACK if dark else None
        icon_color = ft.Colors.WHITE if dark else None

        super().__init__(
            selected_index=selected_index,
            destinations=[
                ft.NavigationBarDestination(
                    icon=(ft.Icon(ft.Icons.PERSON_OUTLINE, color=icon_color) if dark else ft.Icons.PERSON_OUTLINE),
                    selected_icon=(ft.Icon(ft.Icons.PERSON, color=icon_color) if dark else ft.Icons.PERSON),
                    label="User",
                ),
                ft.NavigationBarDestination(
                    icon=(ft.Icon(ft.Icons.HOME_OUTLINED, color=icon_color) if dark else ft.Icons.HOME_OUTLINED),
                    selected_icon=(ft.Icon(ft.Icons.HOME, color=icon_color) if dark else ft.Icons.HOME),
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=(ft.Icon(ft.Icons.SEARCH, color=icon_color) if dark else ft.Icons.SEARCH),
                    label="Explore",
                ),
                ft.NavigationBarDestination(
                    icon=(ft.Icon(ft.Icons.MOVIE_CREATION_OUTLINED, color=icon_color) if dark else ft.Icons.MOVIE_CREATION_OUTLINED),
                    selected_icon=(ft.Icon(ft.Icons.MOVIE_CREATION, color=icon_color) if dark else ft.Icons.MOVIE_CREATION),
                    label="Videos",
                ),
                ft.NavigationBarDestination(
                    icon=(ft.Icon(ft.Icons.EMAIL_OUTLINED, color=icon_color) if dark else ft.Icons.EMAIL_OUTLINED),
                    selected_icon=(ft.Icon(ft.Icons.EMAIL, color=icon_color) if dark else ft.Icons.EMAIL),
                    label="Chats",
                ),
            ],
            on_change=on_change,
            bgcolor=bgcolor,
        )

    def _change_view(self, e: ft.ControlEvent):
        page = e.page
        selected_index = e.control.selected_index
        page.controls.clear()


        from .profileview import ProfileView

        if selected_index == 0:
            page.add(ProfileView(page))


        page.add(NavigationBar(page=page, selected_index=selected_index, dark=(page.theme_mode == ft.ThemeMode.DARK)))
        page.update()


