import flet as ft
import os
import threading
import time
from src.views.playerpanel import PlayerPanel # Importamos el archivo de arriba

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class PlaylistView(ft.Stack):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        self.main_page = page
        self.is_loop = False 
        self.canciones_paths = [] 
        self.indice_actual = -1
        
        if PYGAME_AVAILABLE:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

        # Controles de la barra inferior
        self.btn_play_pause = ft.IconButton(
            icon=ft.Icons.PLAY_ARROW_ROUNDED, icon_size=30, 
            icon_color=ft.Colors.BLACK, bgcolor=ft.Colors.WHITE,
            on_click=self._toggle_reproduccion
        )
        self.txt_titulo = ft.Text("Selecciona una canción", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE, no_wrap=True)
        self.txt_artista = ft.Text("Desconocido", size=13, color=ft.Colors.GREY_400)
        self.lista_canciones = ft.ListView(expand=True, spacing=5)

        # Invocamos el panel pasando 'self' para que reconozca la conexión
        self.reproductor_full = PlayerPanel(self)

        self.controls = [
            ft.Container(
                content=ft.Column([
                    self._crear_header(),
                    ft.Divider(height=1, color="#1E2126"),
                    ft.Container(content=self.lista_canciones, expand=True, padding=ft.Padding.only(left=10, right=10)),
                    self._crear_barra_controles()
                ], expand=True, spacing=0),
                bgcolor="#0F1115",
            ),
            self.reproductor_full 
        ]
        
        self._cargar_musica(inicial=True)
        threading.Thread(target=self._actualizar_progreso_loop, daemon=True).start()

    def _crear_header(self):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=ft.Colors.WHITE, size=35),
                    width=70, height=70, bgcolor="#1E2126", border_radius=15
                ),
                ft.Text("Mi Biblioteca", size=26, weight="bold", color=ft.Colors.WHITE),
            ]),
            padding=ft.Padding.only(left=25, top=40, bottom=20)
        )

    def _crear_barra_controles(self):
        return ft.Container(
            content=ft.Row([
                ft.GestureDetector(
                    content=ft.Column([self.txt_titulo, self.txt_artista], spacing=0, width=220),
                    on_tap=self._abrir_reproductor,
                ),
                self.btn_play_pause,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.BLACK,
            padding=ft.Padding.symmetric(horizontal=20, vertical=15),
            margin=ft.Margin.only(left=5, right=5, bottom=5),
            border_radius=15,
        )

    def _cargar_musica(self, inicial=False):
        self.lista_canciones.controls.clear()
        self.canciones_paths = []
        user_path = os.path.expanduser("~")
        ruta_busqueda = os.path.join(user_path, "Downloads")
        
        if os.path.exists(ruta_busqueda):
            archivos = [f for f in os.listdir(ruta_busqueda) if f.lower().endswith(".mp3")]
            for i, f in enumerate(archivos):
                full_path = os.path.join(ruta_busqueda, f).replace("\\", "/")
                self.canciones_paths.append({"path": full_path, "titulo": f})
                self.lista_canciones.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MUSIC_NOTE_ROUNDED, color=ft.Colors.WHITE),
                        title=ft.Text(f, color=ft.Colors.WHITE, weight="w500", max_lines=1),
                        on_click=lambda e, idx=i: self.reproducir(idx)
                    )
                )
        if not inicial: self.update()

    def reproducir(self, indice):
        self.indice_actual = indice
        cancion = self.canciones_paths[indice]
        
        # ESTO CORRIGE EL REINICIO DEL TIEMPO:
        # Ponemos todo a cero antes de cargar la nueva canción
        self.slider_progreso.value = 0
        self.lbl_tiempo_actual.value = "0:00"
        
        if PYGAME_AVAILABLE:
            pygame.mixer.music.load(cancion["path"])
            pygame.mixer.music.play()
            audio_info = pygame.mixer.Sound(cancion["path"])
            self.slider_progreso.max = audio_info.get_length()
            self.lbl_tiempo_total.value = self._formatear_tiempo(audio_info.get_length())

        self.txt_titulo.value = cancion["titulo"]
        self.full_txt_titulo.value = cancion["titulo"]
        self.btn_play_pause.icon = ft.Icons.PAUSE_ROUNDED
        self.btn_play_pause_full.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
        self.update()

    def _toggle_reproduccion(self, e):
        if self.indice_actual == -1: return
        if PYGAME_AVAILABLE:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
                self.btn_play_pause.icon = ft.Icons.PLAY_ARROW_ROUNDED
                self.reproductor_full.view.btn_play_pause_full.icon = ft.Icons.PLAY_CIRCLE_FILLED_ROUNDED
            else:
                pygame.mixer.music.unpause()
                self.btn_play_pause.icon = ft.Icons.PAUSE_ROUNDED
                self.reproductor_full.view.btn_play_pause_full.icon = ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED
            self.update()

    def _toggle_loop(self, e):
        self.is_loop = not self.is_loop
        # Cambia el color del botón (puedes usar el nombre que le hayas dado al IconButton)
        e.control.icon_color = ft.Colors.BLUE_400 if self.is_loop else ft.Colors.GREY_400
        self.update()

    def _cambiar_cancion(self, delta):
        if not self.canciones_paths: return
        self.indice_actual = (self.indice_actual + delta) % len(self.canciones_paths)
        self.reproducir(self.indice_actual)

    def _actualizar_progreso_loop(self):
        while True:
            if PYGAME_AVAILABLE:
                if pygame.mixer.music.get_busy():
                    pos = pygame.mixer.music.get_pos() / 1000
                    if pos >= 0:
                        self.slider_progreso.value = pos
                        self.lbl_tiempo_actual.value = self._formatear_tiempo(pos)

                        # Solo llamamos a update() si el control ya está en la página
                        try:
                            if self.slider_progreso.page: 
                                self.slider_progreso.update()
                            if self.page:
                                self.page.update()
                        except Exception:
                            # Si falla porque el control se destruyó al cerrar la app, ignoramos
                            pass
                
                # Lógica de fin de canción
                elif self.indice_actual != -1:
                    pos_actual = pygame.mixer.music.get_pos() / 1000
                    if pos_actual == -1 or pos_actual < 0:
                        if self.is_loop:
                            self.reproducir(self.indice_actual)
                        else:
                            self._cambiar_cancion(1)
            
            time.sleep(0.4)

    def _formatear_tiempo(self, segundos):
        mins = int(segundos // 60)
        secs = int(segundos % 60)
        return f"{mins}:{secs:02d}"

    def _seek_music(self, e):
        if PYGAME_AVAILABLE:
            pygame.mixer.music.set_pos(float(e.data))

    def _abrir_reproductor(self, e):
        if self.page.navigation_bar:
            self.page.navigation_bar.visible = False
        self.reproductor_full.bottom = 0
        self.page.update()

    def _cerrar_reproductor(self, e):
        if self.page.navigation_bar:
            self.page.navigation_bar.visible = True
        self.reproductor_full.bottom = -1000
        self.page.update()