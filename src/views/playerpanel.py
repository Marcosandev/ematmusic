import flet as ft

class PlayerPanel(ft.Container):
    def __init__(self, view):
        # Guardamos la referencia a la vista principal para usar sus métodos
        self.view = view
        
        # Definimos los controles exactamente como los tenías
        self.view.full_txt_titulo = ft.Text(
            "Título de la canción", 
            size=22, 
            weight="bold", 
            text_align="center",
            max_lines=1, 
            overflow=ft.TextOverflow.ELLIPSIS 
        )
        
        self.view.full_txt_artista = ft.Text("Desconocido", size=16, color=ft.Colors.GREY_400)
        self.view.slider_progreso = ft.Slider(min=0, max=100, value=0, active_color="#4A90E2", on_change_end=self.view._seek_music)
        self.view.lbl_tiempo_actual = ft.Text("0:00", size=12)
        self.view.lbl_tiempo_total = ft.Text("0:00", size=12)
        self.view.btn_play_pause_full = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED, 
            icon_size=80, 
            on_click=self.view._toggle_reproduccion
        )

        super().__init__(
            content=self._crear_contenido(),
            bgcolor=ft.Colors.BLACK,
            left=0,
            right=0,
            bottom=-1000,
            padding=20,
            expand=True,
            animate_position=ft.Animation(600, ft.AnimationCurve.DECELERATE),
        )

    def _crear_contenido(self):
        return ft.Column([
            ft.Container(
                content=ft.IconButton(ft.Icons.KEYBOARD_ARROW_DOWN, icon_size=35, on_click=self.view._cerrar_reproductor),
                alignment=ft.Alignment.TOP_LEFT,
                padding=ft.Padding.only(bottom=10)
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.MUSIC_NOTE, size=120, color=ft.Colors.BLUE_GREY_400),
                width=300, height=300, border_radius=30, 
                gradient=ft.LinearGradient(
                    colors=[ft.Colors.BLUE_GREY_900, ft.Colors.BLACK], 
                    begin=ft.Alignment(-1, -1)
                ),
                alignment=ft.Alignment.CENTER
            ),
            ft.Container(height=20),
            ft.Column([
                self.view.full_txt_titulo,
                self.view.full_txt_artista,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, width=320),
            
            ft.Column([
                self.view.slider_progreso,
                ft.Row([self.view.lbl_tiempo_actual, self.view.lbl_tiempo_total], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], width=320),
            
            ft.Row([
                ft.IconButton(ft.Icons.FAVORITE, icon_color=ft.Colors.GREY_400),
                ft.IconButton(ft.Icons.SKIP_PREVIOUS_ROUNDED, icon_size=45, on_click=lambda _: self.view._cambiar_cancion(-1)),
                self.view.btn_play_pause_full,
                ft.IconButton(ft.Icons.SKIP_NEXT_ROUNDED, icon_size=45, on_click=lambda _: self.view._cambiar_cancion(1)),
                ft.IconButton(ft.Icons.LOOP, icon_color=ft.Colors.GREY_400, on_click=self.view._toggle_loop),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)