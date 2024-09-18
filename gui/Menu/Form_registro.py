from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_Sesion_BD import ControladorBaseDatos

class RegisterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AWS - Registro")
        self.setStyleSheet("background-color: #2c3e50; color: white; font: 14pt 'Arial';")

        # Configuración del layout principal
        layout_principal = QGridLayout()
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setHorizontalSpacing(20)
        layout_principal.setVerticalSpacing(15)

        # Título
        self.etiqueta_titulo = QLabel("ART - Registro")
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)
        self.etiqueta_titulo.setStyleSheet("font: bold 22pt; margin-bottom: 20px;")
        layout_principal.addWidget(self.etiqueta_titulo, 0, 0, 1, 2)

        # Correo electrónico
        self.etiqueta_correo = QLabel("Correo electrónico")
        self.etiqueta_correo.setStyleSheet("color: white; font-size: 12pt;")
        self.entrada_correo = QLineEdit()
        self.entrada_correo.setPlaceholderText("Correo electrónico (formato nombredeusuario@dominio.com)")
        self.entrada_correo.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        layout_principal.addWidget(self.etiqueta_correo, 1, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.entrada_correo, 1, 1)

        # Nombre
        self.etiqueta_nombre = QLabel("Nombre")
        self.etiqueta_nombre.setStyleSheet("color: white; font-size: 12pt;")
        self.entrada_nombre = QLineEdit()
        self.entrada_nombre.setPlaceholderText("Nombre")
        self.entrada_nombre.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        layout_principal.addWidget(self.etiqueta_nombre, 2, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.entrada_nombre, 2, 1)

        # Apellido
        self.etiqueta_apellido = QLabel("Apellido")
        self.etiqueta_apellido.setStyleSheet("color: white; font-size: 12pt;")
        self.entrada_apellido = QLineEdit()
        self.entrada_apellido.setPlaceholderText("Apellido")
        self.entrada_apellido.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        layout_principal.addWidget(self.etiqueta_apellido, 3, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.entrada_apellido, 3, 1)

        # RUT
        self.etiqueta_rut = QLabel("RUT")
        self.etiqueta_rut.setStyleSheet("color: white; font-size: 12pt;")
        self.entrada_rut = QLineEdit()
        self.entrada_rut.setPlaceholderText("RUT (formato 12345678-9)")
        self.entrada_rut.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        layout_principal.addWidget(self.etiqueta_rut, 4, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.entrada_rut, 4, 1)

        # Contraseña
        self.etiqueta_contrasena = QLabel("Contraseña")
        self.etiqueta_contrasena.setStyleSheet("color: white; font-size: 12pt;")
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setPlaceholderText("Contraseña")
        self.entrada_contrasena.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        self.entrada_contrasena.setEchoMode(QLineEdit.Password)
        layout_principal.addWidget(self.etiqueta_contrasena, 5, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.entrada_contrasena, 5, 1)

        # Botón de mostrar/ocultar contraseña
        self.boton_mostrar_contrasena = QPushButton("Mostrar")
        self.boton_mostrar_contrasena.setStyleSheet("padding: 5px; border-radius: 5px; background-color: #3498db; color: white;")
        self.boton_mostrar_contrasena.setCheckable(True)
        self.boton_mostrar_contrasena.toggled.connect(self.toggle_password_visibility)
        layout_principal.addWidget(self.boton_mostrar_contrasena, 5, 2)

        # Rol
        self.etiqueta_rol = QLabel("Rol")
        self.etiqueta_rol.setStyleSheet("color: white; font-size: 12pt;")
        self.combo_rol = QComboBox()
        self.combo_rol.addItems(["Administrador", "Trabajador", "Supervisor"])
        self.combo_rol.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #34495e;")
        layout_principal.addWidget(self.etiqueta_rol, 6, 0, alignment=Qt.AlignRight)
        layout_principal.addWidget(self.combo_rol, 6, 1)

        # Botón de registro
        self.boton_registrar = QPushButton("Registrarse")
        self.boton_registrar.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #e67e22; color: white;")
        self.boton_registrar.clicked.connect(self.registrar)
        layout_principal.addWidget(self.boton_registrar, 7, 0, 1, 2, alignment=Qt.AlignCenter)

        # Botón de volver
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2980b9; color: white;")
        self.boton_volver.clicked.connect(self.abrir_login)
        layout_principal.addWidget(self.boton_volver, 8, 0, 1, 2, alignment=Qt.AlignCenter)

        self.setLayout(layout_principal)
        self.showMaximized()
    def toggle_password_visibility(self, checked):
        if checked:
            self.entrada_contrasena.setEchoMode(QLineEdit.Normal)
            self.boton_mostrar_contrasena.setText("Ocultar")
        else:
            self.entrada_contrasena.setEchoMode(QLineEdit.Password)
            self.boton_mostrar_contrasena.setText("Mostrar")

    def registrar(self):
        correo = self.entrada_correo.text()
        nombre = self.entrada_nombre.text()
        apellido = self.entrada_apellido.text()
        rut = self.entrada_rut.text()
        contrasena = self.entrada_contrasena.text()
        rol = self.combo_rol.currentText()

        if not self.validar_correo(correo):
            return

        if not self.validar_contrasena(contrasena):
            return

        if not self.validar_rut(rut, rol):
            return

        if correo and nombre and apellido and rut and contrasena and rol:
            controlador_bd = ControladorBaseDatos()
            resultado = controlador_bd.registrar_usuario(correo, nombre, apellido, rut, contrasena, rol)
            
            if "Error" in resultado:
                QMessageBox.warning(self, "Error", resultado)
            else:
                QMessageBox.information(self, "Registro", resultado)
                self.abrir_login()
        else:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")

    def validar_correo(self, correo):
        if "@" not in correo or "." not in correo.split("@")[1]:
            QMessageBox.warning(self, "Error", "El correo electrónico no es válido.")
            return False
        return True

    def validar_contrasena(self, contrasena):
        if (len(contrasena) < 8 or 
            not any(c.isupper() for c in contrasena) or 
            not any(c.isdigit() for c in contrasena) or 
            not any(c in "#$%&" for c in contrasena)):
            QMessageBox.warning(self, "Error", "La contraseña debe contener al menos 8 caracteres, una mayúscula, un número y un símbolo (#, $, %, &, etc.).")
            return False
        return True

    def validar_rut(self, rut, rol):
        controlador_bd = ControladorBaseDatos()
        if controlador_bd._rut_existe(rut, rol):
            QMessageBox.warning(self, "Error", "El RUT ya está registrado.")
            return False
        return True

    def abrir_login(self):
        self.close()
        ventana = ControladorPasos.abrir_login()
        self.app = ventana
        self.app.show()
