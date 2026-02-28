import flet as ft

class MoreView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(spacing=0, expand=True)
        self.main_page = page 
        # Corregido: Usamos ft.Padding.only() para evitar DeprecationWarning
        self.padding = ft.Padding.only(top=10)
        
        # Cargamos los controles iniciales sin llamar a update()
        self.mostrar_menu_principal(es_inicio=True)

    def mostrar_menu_principal(self, es_inicio=False):
        """Limpia la pantalla y dibuja el menú de opciones."""
        self.controls.clear()
        
        # Título de la pantalla
        self.controls.append(
            ft.Container(
                content=ft.Text("Informaciones", size=28, weight="bold"),
                padding=ft.Padding.only(left=20, top=10, bottom=10)
            )
        )

        opciones = [
            ("Ajustes", ft.Icons.SETTINGS, ft.Colors.GREY, self._on_ajustes),
            ("Acerca de", ft.Icons.INFO, ft.Colors.GREY, self._on_acerca),
        ]

        for i, (texto, icono, color, handler) in enumerate(opciones):
            self.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Row([
                            ft.Icon(icono, color=color),
                            ft.Container(width=10),
                            ft.Text(texto, size=18, weight=ft.FontWeight.W_600),
                        ]),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, size=20)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.Padding.symmetric(vertical=12, horizontal=16),
                    on_click=handler,
                    border_radius=10,
                    margin=ft.Margin.symmetric(vertical=2, horizontal=10),
                    ink=True,
                )
            )
            
            if i < len(opciones) - 1:
                self.controls.append(
                    ft.Divider(height=20, color="#1E2126", leading_indent=15, trailing_indent=15)
                )
        
        # IMPORTANTE: Solo actualizamos si NO es la primera vez que se carga
        if not es_inicio:
            self.update()

    def _on_ajustes(self, e):
        self.controls.clear()
        self.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, size=18), 
                        on_click=lambda _: self.mostrar_menu_principal(),
                    ),
                    ft.Text("Ajustes", size=28, weight="bold"),
                ]),
                padding=ft.Padding.only(left=5, bottom=10, top=15)
            )
        )

        self.controls.append(
            ft.ListTile(
                leading=ft.Icon(ft.Icons.BRIGHTNESS_4),
                title=ft.Text("Modo Oscuro"),
                subtitle=ft.Text("Cambia la apariencia de la app"),
                trailing=ft.Switch(
                    value=(self.main_page.theme_mode == ft.ThemeMode.DARK or self.main_page.theme_mode is None),
                    on_change=self._cambiar_tema
                ),
            )
        )
        self.update()

    def _on_acerca(self, e):
        self.controls.clear()
        self.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.IconButton(
                        icon=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, size=18),
                        on_click=lambda _: self.mostrar_menu_principal()
                    ),
                    ft.Text("Acerca de", size=22, weight="bold"),
                ]),
                padding=ft.Padding.only(left=5, bottom=10)
            )
        )

        self.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.MUSIC_NOTE_OUTLINED, size=80, color=ft.Colors.BLUE_GREY_400),
                    ft.Text("EMATMUS♪C", size=24, weight="bold"),
                    ft.Text("Versión 1.0.0", color=ft.Colors.GREY_500),
                    ft.Container(height=20),
                    ft.Text("Creado por Marco Sánchez, Angel Dionel, Ellian Alejandro, Tua.", text_align=ft.TextAlign.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=40,
                alignment=ft.Alignment.CENTER
            )
        )
        self.update()

    def _cambiar_tema(self, e):
        self.main_page.theme_mode = ft.ThemeMode.DARK if e.control.value else ft.ThemeMode.LIGHT
        self.main_page.update()