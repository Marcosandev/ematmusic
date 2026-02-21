import os
import pg8000.native
import pg8000.dbapi
# from psycopg2 import Error # pg8000 has its own Error or use native
from pg8000.dbapi import Error
from dotenv import load_dotenv

load_dotenv()

class PostgresConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD", "password")
        self.database = os.getenv("DB_NAME", "eventmatch")
        self.port = os.getenv("DB_PORT", "5432")
        self.connection = None
        self.connect_to_db()
        self._initialized = True

    def connect_to_db(self):
        """Intenta establecer la conexión con PostgreSQL"""
        try:
            # pg8000 connect call using explicit credentials
            self.connection = pg8000.dbapi.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=int(self.port) # pg8000 expects integer port
            )
            
            # Autocommit is often useful for simple scripts, but let's keep it manual 
            # for transactional control unless specified otherwise. 
            # However, the user's example had 'commit' only for inserts.
            # psycopg2 default is autocommit=False.

            print("✅ Conexión PostgreSQL establecida correctamente.")
            return True

        except Error as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            self.connection = None
            return False

    def execute_query(self, query, params=None, is_insert=False, is_update=False):
        """Ejecuta consultas SQL seguras y maneja reconexión automática."""
        if not self.connection:
            print("⚠️ Conexión PostgreSQL no activa. Intentando reconectar...")
            if not self.connect_to_db():
                print("❌ PostgreSQL Connection not available")
                # Return empty list to prevent 'NoneType has no len()' errors downstream
                # Assuming caller handles empty results gracefully (which they do)
                return []

        try:
            cursor = self.connection.cursor()
        except AttributeError:
            # Handle case where self.connection might be None despite check (rare race condition)
            # or if connection object is invalid
             print("⚠️ Conexión inválida (AttributeError). Reintentando conexión...")
             if self.connect_to_db():
                 cursor = self.connection.cursor()
             else:
                 return []
        try:
            cursor.execute(query, params)
            
            if is_insert or is_update:
                self.connection.commit()
                if is_insert:
                    # In Postgres, to get the last ID, we usually need RETURNING id
                    # if the query has RETURNING id, we can fetch it.
                    if "RETURNING" in query.upper():
                        return cursor.fetchone()[0]
                    return True # Return true if success but no ID returned
                return True
            
            # For SELECT
            # Get column names to mimic dictionary=True from mysql-connector
            columns = [desc[0] for desc in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results

        except Error as e:
            print(f"❌ Error ejecutando consulta: {e}")
            self.connection.rollback()
            return None
        finally:
            cursor.close()

    def __del__(self):
        if self.connection and not self.connection.closed:
            self.connection.close()
            print("🔒 Conexión PostgreSQL cerrada.")
