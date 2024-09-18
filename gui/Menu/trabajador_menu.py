from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_Sesion_BD import ControladorBaseDatos
from Controladores.Controlador_ART_BD import ControladorARTconBD
from datetime import datetime, timedelta

class TrabajadorMenuApp(QMainWindow):
    def __init__(self, rut):
        super().__init__()
        self.setWindowTitle("WWS - Trabajador")
        self.setStyleSheet("background-color: #ecf0f1;")
        self.controlador_bd = ControladorBaseDatos()
        self.controlador_ART_BD = ControladorARTconBD()
        
        self.rut = rut

        # Layout principal
        layout_principal = QHBoxLayout()

        # Frame de la barra lateral
        self.frame_lateral = QFrame()
        self.frame_lateral.setStyleSheet("background-color: #2c3e50;")
        layout_lateral = QVBoxLayout()
        self.frame_lateral.setLayout(layout_lateral)

        # Frame del contenido principal
        self.frame_contenido_principal = QFrame()
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
        self.showMaximized()

    def crear_barra_lateral(self, layout):
        etiqueta_titulo = QLabel("WWS Trabajador")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setFont(QFont("Arial", 18, QFont.Bold))
        etiqueta_titulo.setStyleSheet("color: white; padding: 20px;")
        layout.addWidget(etiqueta_titulo)
        
        boton_formulario = QPushButton("Realizar Formulario")
        boton_formulario.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_formulario.clicked.connect(self.confirmar_realizacion_formulario)
        layout.addWidget(boton_formulario)

        boton_perfil = QPushButton("Perfil")
        boton_perfil.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_perfil.clicked.connect(self.mostrar_perfil)
        layout.addWidget(boton_perfil)

        boton_art_realizadas = QPushButton("ART Realizadas")
        boton_art_realizadas.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_art_realizadas.clicked.connect(self.mostrar_art_realizadas)
        layout.addWidget(boton_art_realizadas)

        layout.addStretch()

    def crear_contenido_principal(self, layout):
        etiqueta_bienvenida = QLabel(f"Bienvenido al menú del Trabajador\nRUT: {self.rut}")
        etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        etiqueta_bienvenida.setStyleSheet("font: bold 24pt; color: #2c3e50; margin-top: 50px;")
        layout.addWidget(etiqueta_bienvenida)

    def mostrar_perfil(self):
        # Limpiar el contenido principal antes de mostrar el perfil
        self.limpiar_contenido_principal()

        # Crear título para la sección de información personal
        titulo_informacion = QLabel("Información Personal")
        titulo_informacion.setAlignment(Qt.AlignCenter)
        titulo_informacion.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_informacion.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.frame_contenido_principal.layout().addWidget(titulo_informacion)

        # Obtener los datos del perfil de la sesión
        rut = self.rut

        # Crear etiquetas para mostrar la información
        etiqueta_rut = QLabel(f"RUT: {rut}")

        # Estilo de las etiquetas
        estilo_etiquetas = "font: 16pt; color: #34495e; padding: 10px;"
        etiqueta_rut.setStyleSheet(estilo_etiquetas)

        # Añadir las etiquetas al layout del contenido principal
        self.frame_contenido_principal.layout().addWidget(etiqueta_rut)

    def mostrar_art_realizadas(self):
        """Muestra las ART realizadas por el trabajador en una tabla."""
        # Limpiar el contenido principal antes de mostrar las ART realizadas
        self.limpiar_contenido_principal()

        # Crear título para la sección de ART realizadas
        titulo_art_realizadas = QLabel("ART Realizadas")
        titulo_art_realizadas.setAlignment(Qt.AlignCenter)
        titulo_art_realizadas.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_art_realizadas.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.frame_contenido_principal.layout().addWidget(titulo_art_realizadas)

        # Crear tabla para mostrar las ART realizadas
        self.tabla_art_realizadas = QTableWidget()
        self.tabla_art_realizadas.setColumnCount(10)  # Ajusta el número de columnas según sea necesario
        self.tabla_art_realizadas.setHorizontalHeaderLabels([
            "ID ART", "RUT Trabajador", "Empresa", "Gerencia", "Fecha", "Hora Inicio",
            "Hora Término", "Superintendencia", "Trabajo a Realizar", "Estado"
        ])
        self.tabla_art_realizadas.setStyleSheet("font: 12pt; color: #34495e;")

        # Obtener las ART realizadas desde la base de datos
        self.cargar_art_realizadas()

        # Añadir la tabla al layout del contenido principal
        self.frame_contenido_principal.layout().addWidget(self.tabla_art_realizadas)

    def cargar_art_realizadas(self):
        rut = self.rut
        art_realizadas = self.controlador_ART_BD.obtener_art_realizadas(rut)

        # Limpia la tabla antes de insertar nuevos datos
        self.tabla_art_realizadas.setRowCount(0)

        # Agrega una fila para cada ART realizada
        for fila, art in enumerate(art_realizadas):
            self.tabla_art_realizadas.insertRow(fila)
            self.tabla_art_realizadas.setItem(fila, 0, QTableWidgetItem(str(art["id_art"])))
            self.tabla_art_realizadas.setItem(fila, 1, QTableWidgetItem(rut))  # Usa el RUT ya que se filtró por este

            self.tabla_art_realizadas.setItem(fila, 2, QTableWidgetItem(art["empresa"]))
            self.tabla_art_realizadas.setItem(fila, 3, QTableWidgetItem(art["gerencia"]))

            # Convertir fecha a cadena si es necesario
            if isinstance(art["fecha"], datetime):
                fecha_str = art["fecha"].strftime("%Y-%m-%d")
            else:
                fecha_str = str(art["fecha"])
            self.tabla_art_realizadas.setItem(fila, 4, QTableWidgetItem(fecha_str))

            # Convertir tiempos a cadena si son timedelta
            for time_key in ["hora_inicio", "hora_termino"]:
                time_value = art[time_key]
                if isinstance(time_value, timedelta):
                    time_str = str(time_value)
                else:
                    time_str = str(time_value)
                self.tabla_art_realizadas.setItem(fila, 5 if time_key == "hora_inicio" else 6, QTableWidgetItem(time_str))

            self.tabla_art_realizadas.setItem(fila, 7, QTableWidgetItem(art["superintendencia"]))
            self.tabla_art_realizadas.setItem(fila, 8, QTableWidgetItem(art["trabajo_realizar"]))
            self.tabla_art_realizadas.setItem(fila, 9, QTableWidgetItem(art["estado"]))

    def limpiar_contenido_principal(self):
        for i in reversed(range(self.frame_contenido_principal.layout().count())):
            widget = self.frame_contenido_principal.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def confirmar_realizacion_formulario(self):
        respuesta = QMessageBox.question(
            self,
            "Confirmación",
            "¿Está seguro de que desea realizar el formulario de ART?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.abrir_formulario_paso1()

    def abrir_formulario_paso1(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso1(self.rut)
        self.app = ventana
        self.app.show()
