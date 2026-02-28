import flet as ft
import datetime
import asyncio
from src.views.playerpanel import PlayerPanel
from src.controllers.playlist_controller import PlaylistController, PYGAME_AVAILABLE

# Intentamos importar pygame para verificar el estado del mixer
try:
    import pygame
except ImportError:
    pygame = None

class PlaylistView(ft.Stack):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.main_page = page
        
        # --- CONFIGURACIÓN DE COLORES DINÁMICOS ---
        es_oscuro = self.main_page.theme_mode == ft.ThemeMode.DARK
        
        # Definimos la paleta de colores según el tema
        self.color_texto_principal = ft.Colors.WHITE if es_oscuro else ft.Colors.BLACK
        self.color_texto_secundario = ft.Colors.GREY_400 if es_oscuro else ft.Colors.GREY_700
        self.color_fondo_header = "#1E2126" if es_oscuro else ft.Colors.GREY_200
        self.color_barra_inferior = ft.Colors.BLACK if es_oscuro else ft.Colors.GREY_100
        self.color_icono_header = ft.Colors.WHITE if es_oscuro else ft.Colors.BLACK
        
        # --- RECUPERACIÓN DE ESTADO ---
        self.indice_actual = (
            self.main_page.session.store.get("musica_indice")
            if self.main_page.session.store.get("musica_indice") is not None
            else -1
        )
        titulo_persistente = (
            self.main_page.session.store.get("musica_titulo") or "Selecciona una canción"
        )
        artista_persistente = (
            self.main_page.session.store.get("musica_artista") or "Desconocido"
        )
        
        self.posicion_salto = self.main_page.session.store.get("musica_pos") or 0
        self.buscando = False
        self.is_loop = False 
        self.canciones_paths = [] 
        
        if PYGAME_AVAILABLE:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

        # Icono de reproducción dinámico
        icono_play = ft.Icons.PLAY_ARROW_ROUNDED
        if PYGAME_AVAILABLE and pygame.mixer.music.get_busy():
            icono_play = ft.Icons.PAUSE_ROUNDED

        # --- CONTROLES DE LA UI ---
        self.btn_play_pause = ft.IconButton(
            icon=icono_play, 
            icon_size=30, 
            icon_color=ft.Colors.BLACK if es_oscuro else ft.Colors.WHITE,
            bgcolor=ft.Colors.WHITE if es_oscuro else ft.Colors.GREY_900,
            on_click=self._toggle_reproduccion
        )
        
        self.txt_titulo = ft.Text(
            titulo_persistente, 
            weight=ft.FontWeight.BOLD, 
            size=16, 
            color=self.color_texto_principal, 
            no_wrap=True
        )
        
        self.txt_artista = ft.Text(
            artista_persistente, 
            size=13, 
            color=self.color_texto_secundario
        )
        
        self.lista_canciones = ft.ListView(expand=True, spacing=5)

        # Invocamos el panel y el controlador
        self.reproductor_full = PlayerPanel(self)
        self.controller = PlaylistController(self)

        # Sincronización del panel si ya hay música
        if self.indice_actual != -1:
            self.reproductor_full.view.full_txt_titulo.value = titulo_persistente
            self.reproductor_full.view.btn_play_pause_full.icon = (
                ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
                if icono_play == ft.Icons.PAUSE_ROUNDED
                else ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
            )

        # Estructura principal
        self.controls = [
            ft.Container(
                content=ft.Column([
                    self._crear_header(),
                    ft.Divider(height=20, color="#1E2126"),
                    ft.Container(
                        content=self.lista_canciones, 
                        expand=True, 
                        padding=ft.Padding.only(left=10, right=10)
                    ),
                    self._crear_barra_controles()
                ], expand=True, spacing=0),
            ),
            self.reproductor_full 
        ]
        
        # Tareas asíncronas de carga
        self.main_page.run_task(self._inicializar_todo)

    async def _inicializar_todo(self):
        """Wrapper para cargar música y sincronizar sin bloquear el hilo principal."""
        await asyncio.to_thread(self.controller.cargar_musica, True)
        await asyncio.to_thread(self.controller.sincronizar_estado_inicial)
        await self.controller.actualizar_progreso_async()

    def _crear_header(self):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=self.color_icono_header, size=35),
                    width=70, height=70, bgcolor=self.color_fondo_header, border_radius=15
                ),
                ft.Text("Mi Biblioteca", size=26, weight="bold", color=self.color_texto_principal),
            ]),
            padding=ft.Padding.only(left=25, top=20, bottom=20)
        )

    def _crear_barra_controles(self):
        return ft.Container(
            content=ft.Row([
                ft.GestureDetector(
                    content=ft.Column([self.txt_titulo, self.txt_artista], spacing=0, width=220),
                    on_tap=self.controller.abrir_reproductor
                ),
                self.btn_play_pause,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=self.color_barra_inferior,
            padding=ft.Padding.symmetric(horizontal=20, vertical=15),
            margin=ft.Margin.only(left=5, right=5, bottom=5),
            border_radius=15,
        )

    def _crear_listtile(self, titulo: str, idx: int, activo: bool):
        # Color dinámico para los ítems de la lista
        es_oscuro = self.main_page.theme_mode == ft.ThemeMode.DARK
        color_item = ft.Colors.BLUE if activo else (ft.Colors.WHITE if es_oscuro else ft.Colors.BLACK)
        
        return ft.ListTile(
            leading=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=color_item),
            title=ft.Text(titulo, color=color_item, weight="w500", max_lines=1),
            on_click=lambda e, i=idx: self.controller.reproducir(i),
        )

    # --- MÉTODOS DE REDIRECCIÓN AL CONTROLADOR ---
    def reproducir(self, indice):
        self.controller.reproducir(indice)

    def _toggle_reproduccion(self, e):
        self.controller.toggle_reproduccion(e)
    
    async def _actualizar_progreso_async(self):
        await self.controller.actualizar_progreso_async()

    def _formatear_tiempo(self, segundos):
        return self.controller.formatear_tiempo(segundos)

    def _sincronizar_estado_inicial(self):
        self.controller.sincronizar_estado_inicial()

    def _on_slider_start(self, e):
        self.buscando = True

    def _on_slider_change(self, e):
        nuevo_valor = float(e.data)
        self.lbl_tiempo_actual.value = self._formatear_tiempo(nuevo_valor)
        self.lbl_tiempo_actual.update()

    def _seek_music(self, e):
        self.controller.seek_music(e)

    def _toggle_favorito(self, e):
        self.controller.toggle_favorito(e)

    def _toggle_loop(self, e):
        self.controller.toggle_loop(e)

    def _cambiar_cancion(self, delta):
        self.controller.cambiar_cancion(delta)

    def _abrir_reproductor(self, e):
        self.controller.abrir_reproductor(e)
        if hasattr(self.main_page, "app_header"):
            self.main_page.app_header.visible = False
            self.main_page.navigation_bar.visible = False
            self.reproductor_full.bottom = 0 
            self.main_page.update()

    def _cerrar_reproductor(self, e):
        self.controller.cerrar_reproductor(e)
        if hasattr(self.main_page, "app_header"):
            self.main_page.app_header.visible = True
            self.main_page.navigation_bar.visible = True
            self.reproductor_full.bottom = -1000
            self.main_page.update()