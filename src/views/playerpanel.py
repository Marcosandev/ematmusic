import flet as ft

class PlayerPanel(ft.Container):
    def __init__(self, view):
        self.view = view
        
        # --- DETECTAR MODO ACTUAL ---
        es_oscuro = self.view.main_page.theme_mode == ft.ThemeMode.DARK
        
        # Paleta de colores dinámica
        color_texto_principal = ft.Colors.WHITE if es_oscuro else ft.Colors.BLACK
        color_texto_secundario = ft.Colors.GREY_400 if es_oscuro else ft.Colors.GREY_600
        color_fondo_panel = ft.Colors.BLACK if es_oscuro else ft.Colors.WHITE
        color_iconos = ft.Colors.WHITE if es_oscuro else ft.Colors.BLACK
        
        # 1. CREAMOS los controles y los guardamos en la clase (self)
        self.slider_progreso = ft.Slider(
            min=0, max=100, value=0, 
            active_color="#4A90E2", 
            on_change_start=self.view._on_slider_start,
            on_change=self.view._on_slider_change,
            on_change_end=self.view._seek_music,
            adaptive=True 
        )
        self.lbl_tiempo_actual = ft.Text("0:00", size=12, color=color_texto_secundario)
        self.lbl_tiempo_total = ft.Text("0:00", size=12, color=color_texto_secundario)
        
        # 2. ASIGNAMOS esas mismas instancias a la vista principal (view)
        self.view.slider_progreso = self.slider_progreso
        self.view.lbl_tiempo_actual = self.lbl_tiempo_actual
        self.view.lbl_tiempo_total = self.lbl_tiempo_total

        # Texto de título y artista dinámicos
        self.view.full_txt_titulo = ft.Text(
            "Título de la canción", size=22, weight="bold", 
            text_align="center", max_lines=1, overflow=ft.TextOverflow.ELLIPSIS,
            color=color_texto_principal 
        )
        self.view.full_txt_artista = ft.Text(
            "Desconocido", size=16, 
            color=color_texto_secundario
        )
        
        # Botón de Play principal (invertido para que resalte)
        self.view.btn_play_pause_full = ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED, 
            icon_size=80, 
            icon_color=color_iconos,
            on_click=self.view._toggle_reproduccion
        )

        # Botón de favorito
        self.btn_fav = ft.IconButton(
            icon=ft.Icons.FAVORITE,
            icon_color=ft.Colors.GREY_400,
            on_click=self.view._toggle_favorito
        )

        # Contenedor principal del Panel
        super().__init__(
            content=self._crear_contenido(color_iconos, es_oscuro),
            bgcolor=color_fondo_panel,
            left=0, right=0, bottom=-1000,
            padding=20, expand=True,
            animate_position=ft.Animation(400, ft.AnimationCurve.DECELERATE), # Un poco más suave
        )

    def _crear_contenido(self, color_iconos, es_oscuro):
        # Ajustamos el degradado del cuadro de la música según el modo
        colores_degradado = (
            [ft.Colors.BLUE_GREY_900, ft.Colors.BLACK] if es_oscuro 
            else [ft.Colors.GREY_300, ft.Colors.GREY_100]
        )

        return ft.Column([
            # Botón para bajar el panel
            ft.Container(
                content=ft.IconButton(
                    ft.Icons.KEYBOARD_ARROW_DOWN, 
                    icon_size=35, 
                    icon_color=color_iconos,
                    on_click=self.view._cerrar_reproductor
                ),
                alignment=ft.Alignment.TOP_LEFT,
            ),
            
            # Carátula/Icono de música
            ft.Container(
                content=ft.Icon(
                    ft.Icons.MUSIC_NOTE, 
                    size=120, 
                    color=ft.Colors.BLUE_GREY_400 if es_oscuro else ft.Colors.BLUE_GREY_200
                ),
                width=300, height=300, border_radius=30, 
                gradient=ft.LinearGradient(
                    colors=colores_degradado, 
                    begin=ft.Alignment(-1, -1)
                ),
                alignment=ft.Alignment.CENTER,
                shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK))
            ),
            
            ft.Container(height=20),
            
            # Textos de la canción
            ft.Column([
                self.view.full_txt_titulo, 
                self.view.full_txt_artista
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5, width=320),
            
            # Slider y Tiempos
            ft.Column([
                self.slider_progreso,
                ft.Row([
                    self.lbl_tiempo_actual, 
                    self.lbl_tiempo_total
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], width=320),
            
            # Controles de reproducción
            ft.Row([
                self.btn_fav,
                ft.IconButton(
                    ft.Icons.SKIP_PREVIOUS_ROUNDED, 
                    icon_size=45, 
                    icon_color=color_iconos,
                    on_click=lambda _: self.view._cambiar_cancion(-1)
                ),
                self.view.btn_play_pause_full,
                ft.IconButton(
                    ft.Icons.SKIP_NEXT_ROUNDED, 
                    icon_size=45, 
                    icon_color=color_iconos,
                    on_click=lambda _: self.view._cambiar_cancion(1)
                ),
                ft.IconButton(
                    ft.Icons.LOOP, 
                    icon_color=ft.Colors.GREY_400, 
                    on_click=self.view._toggle_loop
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10)