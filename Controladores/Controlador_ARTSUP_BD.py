from database.db_connection import MySQLConnection
from mysql.connector import Error

class ControladorARTSUPconBD:
    def __init__(self):
        self.conexion = MySQLConnection()

    def actualizar_supervisor(self, art_id, supervisor):
        query = """
            UPDATE art_trabajador
            SET supervisor = %s
            WHERE id = %s
        """
        params = (supervisor, art_id)
        self.conexion.connect()
        try:
            self.conexion.execute_query(query, params)
            print("Supervisor actualizado exitosamente.")
        except Error as e:
            print(f"Error al actualizar el supervisor: {e}")
        finally:
            self.conexion.close()
    
    def cargar_respuestas_art(self, art_id, paso, codigo_pregunta=None):
        # Construir la consulta base
        query = """
            SELECT numero_pregunta, respuesta_seleccion
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
        """
        
        # Añadir condición para el código de pregunta si se proporciona
        if codigo_pregunta:
            query += " AND numero_pregunta = %s"
            params = (art_id, paso, codigo_pregunta)
        else:
            query += " AND numero_pregunta LIKE %s"
            params = (art_id, paso, 'TR%')

        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Construir el diccionario de respuestas
                respuestas = {row[0]: row[1] for row in resultados}
                
                return respuestas
            else:
                return {}
        except Error as e:
            print(f"Error al cargar las respuestas: {e}")
            return {}
        finally:
            self.conexion.close()

    def cargar_respuestas_artRC(self, art_id, paso, codigo_pregunta=None):
        # Construir la consulta base
        query = """
            SELECT numero_pregunta, respuesta_seleccion
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
            AND numero_pregunta LIKE 'RC%'
        """
        
        # Añadir condición para el código de pregunta si se proporciona
        if codigo_pregunta:
            query += " AND numero_pregunta = %s"
            params = (art_id, paso, codigo_pregunta)
        else:
            params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Construir el diccionario de respuestas
                respuestas = {row[0]: row[1] for row in resultados}
                
                return respuestas
            else:
                return {}
        except Error as e:
            print(f"Error al cargar las respuestas: {e}")
            return {}
        finally:
            self.conexion.close()

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
            if '1062' in str(e):  
                return "Error: La respuesta ya está registrada."
            return f"Error al insertar la respuesta: {e}"
        finally:
            self.conexion.close()

    def obtener_codigo_rc(self, art_id, paso):
        # Construir la consulta base
        query = """
            SELECT DISTINCT numero_pregunta
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
            AND numero_pregunta LIKE 'RC%'
        """
        params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Obtener el primer código de pregunta si existe
                if resultados:
                    return resultados[0][0]  
                else:
                    return None  
            else:
                return None
        except Error as e:
            print(f"Error al obtener los códigos RC: {e}")
            return None
        finally:
            self.conexion.close()

    def obtener_respuestas_riesgos(self, art_id, paso):
        # Construir la consulta base
        query = """
            SELECT numero_pregunta, respuesta_texto
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
            AND numero_pregunta LIKE 'riesgo%'
        """
        params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Convertir los resultados a un diccionario
                respuestas_riesgos = {row[0]: row[1] for row in resultados}
                return respuestas_riesgos
            else:
                return {}
        except Error as e:
            print(f"Error al obtener respuestas de riesgos: {e}")
            return {}
        finally:
            self.conexion.close()

    def obtener_respuestas_medidas_control(self, art_id, paso):
        # Construir la consulta base
        query = """
            SELECT numero_pregunta, respuesta_texto
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
            AND numero_pregunta LIKE 'medida_control%'
        """
        params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Convertir los resultados a un diccionario
                respuestas_medidas_control = {row[0]: row[1] for row in resultados}
                return respuestas_medidas_control
            else:
                return {}
        except Error as e:
            print(f"Error al obtener respuestas de medidas de control: {e}")
            return {}
        finally:
            self.conexion.close()

    def obtener_respuesta_paso4(self, art_id, paso):
        # Consulta para obtener las respuestas del trabajador en el paso 4
        query = """
            SELECT numero_pregunta, respuesta_seleccion
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
        """
        params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Convertir los resultados a un diccionario
                respuestas_paso4 = {row[0]: row[1] for row in resultados}
                return respuestas_paso4
            else:
                return {}
        except Error as e:
            print(f"Error al obtener respuestas del paso 4: {e}")
            return {}
        finally:
            self.conexion.close()

    def obtener_respuesta_paso4_TS(self, art_id, paso):
        # Consulta para obtener las respuestas relacionadas con trabajo simultáneo en el paso 4
        query = """
            SELECT numero_pregunta, respuesta_texto
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = %s 
            AND tipo_respuesta = 'trabajador'
            AND numero_pregunta = 'trabajo simultaneo'
        """
        params = (art_id, paso)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Convertir los resultados a un diccionario
                respuestas_TS = {row[0]: row[1] for row in resultados}
                return respuestas_TS
            else:
                return {}
        except Error as e:
            print(f"Error al obtener respuestas de trabajo simultáneo: {e}")
            return {}
        finally:
            self.conexion.close()

    def obtener_respuesta_paso5(self, art_id):
        # Consulta para obtener las respuestas del trabajador en el paso 5
        query = """
            SELECT numero_pregunta, respuesta_texto
            FROM respuesta_art
            WHERE art_id = %s 
            AND paso = 5 
            AND tipo_respuesta = 'trabajador'
        """
        params = (art_id,)
        
        print("Consulta SQL:", query)
        print("Parámetros:", params)

        self.conexion.connect()
        try:
            cursor = self.conexion.get_cursor()
            if cursor:
                cursor.execute(query, params)
                resultados = cursor.fetchall()
                
                # Mostrar los resultados para depurar
                print("Resultados:", resultados)
                
                # Convertir los resultados a un diccionario
                respuestas_paso5 = {row[0]: row[1] for row in resultados}
                return respuestas_paso5
            else:
                return {}
        except Error as e:
            print(f"Error al obtener respuestas del paso 5: {e}")
            return {}
        finally:
            self.conexion.close()
