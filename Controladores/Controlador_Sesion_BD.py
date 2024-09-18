from database.db_connection import MySQLConnection
import bcrypt
from mysql.connector import Error

class ControladorSesionconBD:
    def __init__(self):
        self.conexion = MySQLConnection()

    def _hash_password(self, password):
        # Utiliza bcrypt para hash de contraseñas
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def registrar_usuario(self, correo, nombre, apellido, rut, contrasena, rol):
        if self._rut_existe(rut, rol):
            return "Error: El RUT ya está registrado."  # RUT ya existe
        
        if self._correo_existe(correo):
            return "Error: El correo electrónico ya está registrado."  # Correo ya existe
        
        self.conexion.connect()
        
        # Hash de la contraseña
        contrasena_hash = self._hash_password(contrasena)

        if rol == "Administrador":
            query = "INSERT INTO administrador (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        elif rol == "Trabajador":
            query = "INSERT INTO trabajador (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        elif rol == "Supervisor":
            query = "INSERT INTO supervisor (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        else:
            # Rol no válido
            return "Error: Rol no válido."
        
        params = (rut, nombre, apellido, correo, contrasena_hash)
        
        try:
            self.conexion.execute_query(query, params)
            return "Registro exitoso."
        except Error as e:
            if '1062' in str(e):  # Código de error para clave duplicada
                return "Error: El RUT o correo ya están registrados."
            return f"Error al registrar el usuario: {e}"
        finally:
            self.conexion.close()

    def _rut_existe(self, rut, rol):
        self.conexion.connect()
        if rol == "Administrador":
            query = "SELECT 1 FROM administrador WHERE rut = %s"
        elif rol == "Trabajador":
            query = "SELECT 1 FROM trabajador WHERE rut = %s"
        elif rol == "Supervisor":
            query = "SELECT 1 FROM supervisor WHERE rut = %s"
        else:
            return False

        result = self.conexion.execute_query(query, (rut,), fetch_one=True)
        self.conexion.close()

        return result is not None

    def _correo_existe(self, correo):
        self.conexion.connect()
        query = "SELECT 1 FROM administrador WHERE email = %s UNION SELECT 1 FROM trabajador WHERE email = %s UNION SELECT 1 FROM supervisor WHERE email = %s"
        result = self.conexion.execute_query(query, (correo, correo, correo), fetch_one=True)
        self.conexion.close()

        return result is not None

    def _verificar_contrasena(self, contrasena_proporcionada, contrasena_hash):
        # Verifica la contraseña utilizando bcrypt
        return bcrypt.checkpw(contrasena_proporcionada.encode('utf-8'), contrasena_hash.encode('utf-8'))

    def iniciar_sesion(self, rut, contrasena, rol):
        self.conexion.connect()
        
        if rol == "Administrador":
            query = "SELECT contrasena_hash FROM administrador WHERE rut = %s"
        elif rol == "Trabajador":
            query = "SELECT contrasena_hash FROM trabajador WHERE rut = %s"
        elif rol == "Supervisor":
            query = "SELECT contrasena_hash FROM supervisor WHERE rut = %s"
        else:
            self.conexion.close()
            return False, "Rol no válido"

        params = (rut,)

        try:
            result = self.conexion.execute_query(query, params, fetch_one=True)
            if result:
                contrasena_hash = result[0]
                if self._verificar_contrasena(contrasena, contrasena_hash):
                    return True, "Inicio de sesión exitoso"
                else:
                    return False, "Contraseña incorrecta"
            else:
                return False, "El RUT no está registrado"
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
            return False, "Error en el proceso de inicio de sesión"
        finally:
            self.conexion.close()

from database.db_connection import MySQLConnection
import bcrypt
from mysql.connector import Error

class ControladorBaseDatos:
    def __init__(self):
        self.conexion = MySQLConnection()

    def _hash_password(self, password):
        # Utiliza bcrypt para hash de contraseñas
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def registrar_usuario(self, correo, nombre, apellido, rut, contrasena, rol):
        if self._rut_existe(rut, rol):
            return "Error: El RUT ya está registrado."  # RUT ya existe
        
        if self._correo_existe(correo):
            return "Error: El correo electrónico ya está registrado."  # Correo ya existe
        
        self.conexion.connect()
        
        # Hash de la contraseña
        contrasena_hash = self._hash_password(contrasena)

        if rol == "Administrador":
            query = "INSERT INTO administrador (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        elif rol == "Trabajador":
            query = "INSERT INTO trabajador (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        elif rol == "Supervisor":
            query = "INSERT INTO supervisor (rut, nombre, apellido, email, contrasena_hash) VALUES (%s, %s, %s, %s, %s)"
        else:
            # Rol no válido
            return "Error: Rol no válido."
        
        params = (rut, nombre, apellido, correo, contrasena_hash)
        
        try:
            self.conexion.execute_query(query, params)
            return "Registro exitoso."
        except Error as e:
            if '1062' in str(e):  # Código de error para clave duplicada
                return "Error: El RUT o correo ya están registrados."
            return f"Error al registrar el usuario: {e}"
        finally:
            self.conexion.close()

    def _rut_existe(self, rut, rol):
        self.conexion.connect()
        if rol == "Administrador":
            query = "SELECT 1 FROM administrador WHERE rut = %s"
        elif rol == "Trabajador":
            query = "SELECT 1 FROM trabajador WHERE rut = %s"
        elif rol == "Supervisor":
            query = "SELECT 1 FROM supervisor WHERE rut = %s"
        else:
            return False

        result = self.conexion.execute_query(query, (rut,), fetch_one=True)
        self.conexion.close()

        return result is not None

    def _correo_existe(self, correo):
        self.conexion.connect()
        query = "SELECT 1 FROM administrador WHERE email = %s UNION SELECT 1 FROM trabajador WHERE email = %s UNION SELECT 1 FROM supervisor WHERE email = %s"
        result = self.conexion.execute_query(query, (correo, correo, correo), fetch_one=True)
        self.conexion.close()

        return result is not None

    def _verificar_contrasena(self, contrasena_proporcionada, contrasena_hash):
        # Verifica la contraseña utilizando bcrypt
        return bcrypt.checkpw(contrasena_proporcionada.encode('utf-8'), contrasena_hash.encode('utf-8'))

    def iniciar_sesion(self, rut, contrasena, rol):
        self.conexion.connect()
        
        if rol == "Administrador":
            query = "SELECT contrasena_hash FROM administrador WHERE rut = %s"
        elif rol == "Trabajador":
            query = "SELECT contrasena_hash FROM trabajador WHERE rut = %s"
        elif rol == "Supervisor":
            query = "SELECT contrasena_hash FROM supervisor WHERE rut = %s"
        else:
            self.conexion.close()
            return False, "Rol no válido"

        params = (rut,)

        try:
            result = self.conexion.execute_query(query, params, fetch_one=True)
            if result:
                contrasena_hash = result[0]
                if self._verificar_contrasena(contrasena, contrasena_hash):
                    return True, "Inicio de sesión exitoso"
                else:
                    return False, "Contraseña incorrecta"
            else:
                return False, "El RUT no está registrado"
        except Error as e:
            print(f"Error al iniciar sesión: {e}")
            return False, "Error en el proceso de inicio de sesión"
        finally:
            self.conexion.close()
