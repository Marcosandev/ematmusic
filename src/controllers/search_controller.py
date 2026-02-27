from src.models.postgres import PostgresConnector # Ajusta la ruta si está en otra carpeta

class SearchController:
    def __init__(self):
        self.db = PostgresConnector()

    def search_songs(self, query):
        sql = """
            SELECT id, titulo as title, artista as artist, genero as genero, url
            FROM canciones 
            WHERE titulo ILIKE %s OR artista ILIKE %s 
            LIMIT 20
        """
        params = [f"%{query}%", f"%{query}%"]
        results = self.db.execute_query(sql, params)
        return results if results is not None else []

    def search_artists(self, query):
        sql = """
            SELECT id, nombre as name, imagen_url as image 
            FROM artistas 
            WHERE nombre ILIKE %s 
            LIMIT 15
        """
        params = [f"%{query}%"]
        results = self.db.execute_query(sql, params)
        return results if results is not None else []