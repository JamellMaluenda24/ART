from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos  # Importar el gestor de formularios

class AdminMenuApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CIQUIMET - Administrador")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Layout principal
        layout_principal = QHBoxLayout()

        # Frame de la barra lateral
        self.frame_lateral = QWidget()
        self.frame_lateral.setStyleSheet("background-color: #2c3e50;")
        layout_lateral = QVBoxLayout()
        self.frame_lateral.setLayout(layout_lateral)

        # Frame del contenido principal
        self.frame_contenido_principal = QWidget()
        layout_contenido_principal = QVBoxLayout()
        self.frame_contenido_principal.setLayout(layout_contenido_principal)

        # Añadir la barra lateral y el contenido principal al layout principal
        layout_principal.addWidget(self.frame_lateral, 1)
        layout_principal.addWidget(self.frame_contenido_principal, 4)

        # Configurar la ventana principal
        contenedor_principal = QWidget()
        contenedor_principal.setLayout(layout_principal)
        self.setCentralWidget(contenedor_principal)

        # Crear elementos de la barra lateral
        self.crear_barra_lateral(layout_lateral)

        # Crear contenido principal inicial
        self.crear_contenido_principal(layout_contenido_principal)

    def crear_barra_lateral(self, layout):
        # Foto de perfil (placeholder)
        etiqueta_foto_perfil = QLabel("Foto de Perfil")
        etiqueta_foto_perfil.setAlignment(Qt.AlignCenter)
        etiqueta_foto_perfil.setStyleSheet("color: white; margin-top: 20px;")
        layout.addWidget(etiqueta_foto_perfil)

        # Botón de Perfil
        boton_perfil = QPushButton("Perfil")
        boton_perfil.setStyleSheet("padding: 15px; background-color: #34495e; color: white;")
        boton_perfil.clicked.connect(self.mostrar_perfil)
        layout.addWidget(boton_perfil)

        # Botón de Configuración
        boton_configuracion = QPushButton("Configuración")
        boton_configuracion.setStyleSheet("padding: 15px; background-color: #34495e; color: white;")
        boton_configuracion.clicked.connect(self.mostrar_configuracion)
        layout.addWidget(boton_configuracion)

    def crear_contenido_principal(self, layout):
        etiqueta_bienvenida = QLabel("Bienvenido al menú del Administrador")
        etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        etiqueta_bienvenida.setStyleSheet("font: bold 16pt; color: #2c3e50; margin-top: 20px;")
        layout.addWidget(etiqueta_bienvenida)

    def mostrar_perfil(self):
        self.limpiar_contenido_principal()
        etiqueta_perfil = QLabel("Perfil")
        etiqueta_perfil.setAlignment(Qt.AlignCenter)
        etiqueta_perfil.setStyleSheet("font: bold 14pt; color: #2c3e50; margin-top: 20px;")
        self.frame_contenido_principal.layout().addWidget(etiqueta_perfil)

    def mostrar_configuracion(self):
        self.limpiar_contenido_principal()
        etiqueta_configuracion = QLabel("Configuración")
        etiqueta_configuracion.setAlignment(Qt.AlignCenter)
        etiqueta_configuracion.setStyleSheet("font: bold 14pt; color: #2c3e50; margin-top: 20px;")
        self.frame_contenido_principal.layout().addWidget(etiqueta_configuracion)

    def limpiar_contenido_principal(self):
        for i in reversed(range(self.frame_contenido_principal.layout().count())):
            widget = self.frame_contenido_principal.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

if __name__ == "__main__":
    app = QApplication([])
    ventana_admin = AdminMenuApp()
    ventana_admin.show()
    app.exec_()
