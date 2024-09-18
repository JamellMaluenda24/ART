from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QComboBox, 
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from gui.Menu.admin_menu import AdminMenuApp
from gui.Menu.trabajador_menu import TrabajadorMenuApp
from gui.Menu.supervisor_menu import SupervisorMenuApp
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_Sesion_BD import ControladorBaseDatos

class AplicacionLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WWS - Login")
        self.setWindowIcon(QIcon("img/Logo/WSS64x64.png"))
        self.setStyleSheet("background-color: #2c3e50; color: white; font: 14pt 'Arial';")

        # Configuración del layout principal
        self.setup_ui()

    def setup_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(50, 50, 50, 50)  # Añadir márgenes para mejor espaciado

        # Layout para el logo centrado
        layout_logo = QVBoxLayout()
        layout_logo.setAlignment(Qt.AlignCenter)

        # Crear y añadir el logo centrado
        self.logo_label = QLabel()
        pixmap = QPixmap("img/Logo/WSSlogo.png")  # Reemplaza con la ruta a tu logo
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(200, 100)  # Ajustar tamaño según el logo
        layout_logo.addWidget(self.logo_label)

        layout_principal.addLayout(layout_logo)

        # Título
        self.etiqueta_titulo = QLabel("ART - Login")
        self.etiqueta_titulo.setAlignment(Qt.AlignCenter)
        self.etiqueta_titulo.setStyleSheet("font: bold 20pt; margin-bottom: 20px;")
        layout_principal.addWidget(self.etiqueta_titulo)

        # Campo de RUT
        self.entrada_rut = QLineEdit()
        self.entrada_rut.setPlaceholderText("RUT")
        self.entrada_rut.setStyleSheet("padding: 10px; border-radius: 5px;")
        layout_principal.addWidget(self.entrada_rut)

        # Contraseña
        self.entrada_contrasena = QLineEdit()
        self.entrada_contrasena.setPlaceholderText("Contraseña")
        self.entrada_contrasena.setEchoMode(QLineEdit.Password)
        self.entrada_contrasena.setStyleSheet("padding: 10px; border-radius: 5px;")
        layout_principal.addWidget(self.entrada_contrasena)

        # Rol
        self.combobox_rol = QComboBox()
        self.combobox_rol.addItems(["Administrador", "Trabajador", "Supervisor"])
        self.combobox_rol.setStyleSheet("padding: 10px; border-radius: 5px;")
        layout_principal.addWidget(self.combobox_rol)

        # Botón de Ingreso
        self.boton_ingresar = QPushButton("Ingresar")
        self.boton_ingresar.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #e67e22; color: white;")
        self.boton_ingresar.clicked.connect(self.iniciar_sesion)
        layout_principal.addWidget(self.boton_ingresar)

        # Botón de Registro
        self.boton_registrar = QPushButton("Registrarse")
        self.boton_registrar.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #2980b9; color: white;")
        self.boton_registrar.clicked.connect(self.registrar)
        layout_principal.addWidget(self.boton_registrar)

        # Información adicional
        self.etiqueta_info = QLabel(
            "Estimados usuarios,\n\n"
            "Disponen de una plataforma para realizar el ART diario. "
            "Para acceder, deben identificarse con su RUT y contraseña, la cual es personal e intransferible.\n\n"
            "Tienen dos opciones:\n"
            "1. ART: Completar el formulario digital y enviarlo para respaldo.\n"
            "2. DOCUMENTOS: Acceder a la Guía de Controles Críticos y el Formato ART."
        )
        self.etiqueta_info.setStyleSheet(
            "font: 10pt; margin-top: 20px; padding: 15px; background-color: #34495e; border-radius: 10px; color: #ecf0f1;"
        )
        self.etiqueta_info.setWordWrap(True)
        self.etiqueta_info.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(self.etiqueta_info)

        # Configuración del contenedor y la ventana
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Instancia del controlador de base de datos
        self.controlador_bd = ControladorBaseDatos()
        self.showMaximized()
        
    def iniciar_sesion(self):
        rut = self.entrada_rut.text()
        contrasena = self.entrada_contrasena.text()
        rol = self.combobox_rol.currentText()

        if not rut or not contrasena or not rol:
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        # Intentar iniciar sesión
        exito, mensaje = self.controlador_bd.iniciar_sesion(rut, contrasena, rol)

        if exito:
            self.abrir_menu_aplicacion(rol,rut)
        else:
            QMessageBox.warning(self, "Error", mensaje)

    def abrir_menu_aplicacion(self, rol,rut):
        self.hide()
        if rol == "Administrador":
            self.app = AdminMenuApp(rut)
        elif rol == "Trabajador":
            self.app = TrabajadorMenuApp(rut)
        elif rol == "Supervisor":
            self.app = SupervisorMenuApp(rut)
        self.app.show()

    def registrar(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_registro()
        self.app = ventana
        self.app.show()

if __name__ == "__main__":
    app = QApplication([])
    aplicacion_login = AplicacionLogin()
    aplicacion_login.show()
    app.exec_()
