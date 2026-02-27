from src.models.postgres import PostgresConnector

class AlbumController:
    def __init__(self):
        self.db = PostgresConnector()

    def get_all_albums(self):
        """Obtiene todos los álbumes para la vista de cuadrícula."""
        sql = "SELECT id, nombre, artista, color_hex FROM albumes ORDER BY nombre ASC"
        results = self.db.execute_query(sql)
        return results if results is not None else []

    def get_songs_by_album(self, album_id):
        sql = """
            SELECT titulo as title, artista as artist, url 
            FROM canciones 
            WHERE album_id = %s
        """
        params = [album_id]
        results = self.db.execute_query(sql, params)
        return results if results is not None else []