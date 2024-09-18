import mysql.connector
from mysql.connector import Error

class MySQLConnection:
    #modificar parametros de acuerdo al pc propio
    def __init__(self, host='localhost', user='root', password='jamell507', database='prueba1'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            # Configura la conexión
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            if self.connection.is_connected():
                print("Conexión exitosa a MySQL")

                # Verificar la base de datos a la que está conectado
                cursor = self.connection.cursor()
                cursor.execute("SELECT DATABASE();")
                base_de_datos = cursor.fetchone()
                print(f"Conectado a la base de datos: {base_de_datos[0]}")

        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.connection = None
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")

    def get_cursor(self):
        if self.connection and self.connection.is_connected():
            return self.connection.cursor()
        else:
            print("No hay conexión activa para obtener el cursor")
            return None

    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        cursor = self.get_cursor()
        if cursor:
            try:
                cursor.execute(query, params)
                if fetch_one:
                    result = cursor.fetchone()
                    self.connection.commit()
                    return result
                elif fetch_all:
                    result = cursor.fetchall()
                    self.connection.commit()
                    return result
                else:
                    self.connection.commit()
                    print("Consulta ejecutada exitosamente")
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
            finally:
                cursor.close()
        else:
            print("No se pudo obtener el cursor para ejecutar la consulta")


