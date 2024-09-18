from database.db_connection import MySQLConnection
from mysql.connector import Error

class ControladorARTconBD:
    def __init__(self):
        self.conexion = MySQLConnection()

    def guardar_art(self, trabajador_rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar):
        self.conexion.connect()

        query = """
            INSERT INTO art_trabajador
            (trabajador_rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (trabajador_rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar)

        try:
            self.conexion.execute_query(query, params)
            print("ART guardado exitosamente.")
            id_art = self.obtener_id_art_trabajador()
            return id_art
        
        except Error as e:
            print(f"Error al guardar ART: {e}")
            return None
        
        finally:
            self.conexion.close()

    def obtener_id_art_trabajador(self):
        query = "SELECT LAST_INSERT_ID()"
        
        try:
            result = self.conexion.execute_query(query, fetch_one=True)
            if result:
                return result[0]
            else:
                return None
        except Error as e:
            print(f"Error al obtener la ID de ART: {e}")
            return None
        
    def insertar_respuesta(self, art_id, tipo_respuesta, paso, numero_pregunta, respuesta_seleccion=None, respuesta_texto=None):
        query = """
            INSERT INTO respuesta_art (art_id, tipo_respuesta, paso, numero_pregunta, respuesta_seleccion, respuesta_texto)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (art_id, tipo_respuesta, paso, numero_pregunta, respuesta_seleccion, respuesta_texto)
        self.conexion.connect()
        try:
            self.conexion.execute_query(query, params)
            return "Respuesta insertada exitosamente."
        except Error as e:
            if '1062' in str(e):  # Código de error para clave duplicada
                return "Error: La respuesta ya está registrada."
            return f"Error al insertar la respuesta: {e}"
        finally:
            self.conexion.close()

    def insertar_respuesta_texto(self, art_id, tipo_respuesta, paso, numero_pregunta, respuesta_texto):
        query = """
            INSERT INTO respuesta_art (art_id, tipo_respuesta, paso, numero_pregunta, respuesta_texto)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (art_id, tipo_respuesta, paso, numero_pregunta, respuesta_texto)
        self.conexion.connect()
        try:
            # Ejecutar la consulta
            self.conexion.execute_query(query, params)
            return "Respuesta de texto insertada exitosamente."
        except Error as e:
            if '1062' in str(e):  # Código de error para clave duplicada
                return "Error: La respuesta ya está registrada."
            return f"Error al insertar la respuesta de texto: {e}"
        finally:
            self.conexion.close()

    def art_en_espera(self, art_id):
        self.conexion.connect()

        query = """
            UPDATE art_trabajador
            SET estado = 'en espera'
            WHERE id = %s
        """
        params = (art_id,)

        try:
            self.conexion.execute_query(query, params)
            print("Estado de ART actualizado a 'en espera'.")
        except Error as e:
            print(f"Error al actualizar el estado de ART: {e}")
        finally:
            self.conexion.close()

    def art_aprobada(self, art_id):
        self.conexion.connect()

        query = """
            UPDATE art_trabajador
            SET estado = 'Aprobada'
            WHERE id = %s
        """
        params = (art_id,)

        try:
            self.conexion.execute_query(query, params)
            print("Estado de ART actualizado a 'Aprobada'.")
        except Error as e:
            print(f"Error al actualizar el estado de ART: {e}")
        finally:
            self.conexion.close()
    #muestra las art del trabajador que el realizo
    def obtener_art_realizadas(self, rut):
        query = """
            SELECT id AS id_art, trabajador_rut, fecha, empresa, gerencia, hora_inicio, hora_termino, superintendencia, trabajo_realizar, estado
            FROM art_trabajador
            WHERE trabajador_rut = %s
        """
        params = (rut,)  # Asegúrate de que params sea una tupla
        self.conexion.connect()

        try:
            result = self.conexion.execute_query(query, params, fetch_all=True)
            if result:
                # Convierte las filas en un formato de diccionario
                return [
                    {
                        "id_art": row[0],
                        "trabajador_rut": row[1],
                        "fecha": row[2],
                        "empresa": row[3],
                        "gerencia": row[4],
                        "hora_inicio": row[5],
                        "hora_termino": row[6],
                        "superintendencia": row[7],
                        "trabajo_realizar": row[8],
                        "estado": row[9]
                    }
                    for row in result
                ]
            return []
        except Error as e:
            print(f"Error al obtener ART realizadas: {e}")
            return []
        finally:
            self.conexion.close()


    def obtener_art_a_responder(self):
        self.conexion.connect()

        query = """
            SELECT id AS id_art, trabajador_rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar, estado
            FROM art_trabajador
            WHERE estado = 'en espera'
        """
        
        try:
            result = self.conexion.execute_query(query, fetch_all=True)
            if result:
                # Convierte las filas en un formato de diccionario
                return [
                    {
                        "id_art": row[0],
                        "trabajador_rut": row[1],
                        "empresa": row[2],
                        "gerencia": row[3],
                        "fecha": row[4],
                        "hora_inicio": row[5],
                        "hora_termino": row[6],
                        "superintendencia": row[7],
                        "trabajo_realizar": row[8],
                        "estado": row[9]  # Corregido para reflejar el índice correcto
                    }
                    for row in result
                ]
            return []
        except Error as e:
            print(f"Error al obtener ARTs a responder: {e}")
            return []
        finally:
            self.conexion.close()
    
    def obtener_datos_art(self, id_art):
            self.conexion.connect()

            query = """
                SELECT id AS id_art, trabajador_rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar, estado
                FROM art_trabajador
                WHERE id = %s
            """
            params = (id_art,)

            try:
                result = self.conexion.execute_query(query, params, fetch_one=True)
                if result:
                    return {
                        "id_art": result[0],
                        "trabajador_rut": result[1],
                        "empresa": result[2],
                        "gerencia": result[3],
                        "fecha": result[4],
                        "hora_inicio": result[5],
                        "hora_termino": result[6],
                        "superintendencia": result[7],
                        "trabajo_realizar": result[8],
                        "estado": result[9]
                    }
                return None
            except Error as e:
                print(f"Error al obtener los datos de ART: {e}")
                return None
            finally:
                self.conexion.close()
    def obtener_art_realizadas_supervisor(self):
            self.conexion.connect()

            query = """
                SELECT id AS id_art, trabajador_rut, fecha, empresa, gerencia, hora_inicio, hora_termino, superintendencia, trabajo_realizar, estado
                FROM art_trabajador
            """
            
            try:
                result = self.conexion.execute_query(query, fetch_all=True)
                if result:
                    # Convierte las filas en un formato de diccionario
                    return [
                        {
                            "id_art": row[0],
                            "trabajador_rut": row[1],
                            "fecha": row[2],
                            "empresa": row[3],
                            "gerencia": row[4],
                            "hora_inicio": row[5],
                            "hora_termino": row[6],
                            "superintendencia": row[7],
                            "trabajo_realizar": row[8],
                            "estado": row[9]
                        }
                        for row in result
                    ]
                return []
            except Error as e:
                print(f"Error al obtener ART realizadas: {e}")
                return []
            finally:
                self.conexion.close()

    def obtener_art_aprobadas_supervisor(self):
        self.conexion.connect()

        query = """
            SELECT id AS id_art, trabajador_rut, fecha, empresa, gerencia, hora_inicio, hora_termino, superintendencia, trabajo_realizar, estado
            FROM art_trabajador
            WHERE estado = 'Aprobada'
        """
        
        try:
            result = self.conexion.execute_query(query, fetch_all=True)
            if result:
                # Convierte las filas en un formato de diccionario
                return [
                    {
                        "id_art": row[0],
                        "trabajador_rut": row[1],
                        "fecha": row[2],
                        "empresa": row[3],
                        "gerencia": row[4],
                        "hora_inicio": row[5],
                        "hora_termino": row[6],
                        "superintendencia": row[7],
                        "trabajo_realizar": row[8],
                        "estado": row[9]
                    }
                    for row in result
                ]
            return []
        except Error as e:
            print(f"Error al obtener ART aprobadas: {e}")
            return []
        finally:
            self.conexion.close()
