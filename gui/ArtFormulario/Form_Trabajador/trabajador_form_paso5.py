from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QComboBox, 
    QPushButton, QVBoxLayout, QFormLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD

class FormularioPaso5Trabajador(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.setWindowTitle("Paso 5: Condiciones Físicas y Psicológicas para Realizar el Trabajo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")  # Fondo gris claro

        # Configuración de la ventana
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout()
        self.layout_principal.setContentsMargins(20, 20, 20, 20)
        self.layout_principal.setSpacing(10)
        self.widget_central.setLayout(self.layout_principal)

        # Crear el título y los formularios
        self.crear_titulo()
        self.crear_frame_formulario()
        self.crear_frame_botones()

        self.showMaximized()

    def crear_titulo(self):
        """Crea y configura el título de la ventana."""
        etiqueta_titulo = QLabel("Paso 5: Condiciones Físicas y Psicológicas para Realizar el Trabajo / Validación ART por Equipo Ejecutor")
        etiqueta_titulo.setFont(QFont("Arial", 22, QFont.Bold))
        etiqueta_titulo.setStyleSheet("font: bold 22pt; color: #2c3e50; margin-bottom: 20px;")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        self.layout_principal.addWidget(etiqueta_titulo)

    def crear_frame_formulario(self):
        """Crea y configura el formulario del paso 5."""
        self.frame_formulario = QWidget()
        self.layout_formulario = QFormLayout(self.frame_formulario)
        self.layout_formulario.setLabelAlignment(Qt.AlignRight)
        self.layout_formulario.setSpacing(15)
        self.layout_formulario.setContentsMargins(0, 0, 0, 0)
        self.layout_principal.addWidget(self.frame_formulario)

        # Crear campos del formulario
        self.crear_campos_formulario()

    def crear_campos_formulario(self):
        """Crea los campos del formulario para el paso 5."""
        self.crear_grupo_trabajadores()

    def crear_grupo_trabajadores(self):
        """Crea el grupo de campos relacionados con los trabajadores."""
        # Título del grupo
        etiqueta_trabajadores = QLabel("Información del Trabajador")
        etiqueta_trabajadores.setFont(QFont("Arial", 16, QFont.Bold))
        etiqueta_trabajadores.setStyleSheet("margin-bottom: 20px;")
        self.layout_formulario.addRow(etiqueta_trabajadores)

        # Nombre del trabajador
        etiqueta_nombre_trabajador = QLabel("Nombre:")
        self.entrada_nombre_trabajador = QLineEdit()
        self.entrada_nombre_trabajador.setFont(QFont("Arial", 12))
        self.entrada_nombre_trabajador.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.layout_formulario.addRow(etiqueta_nombre_trabajador, self.entrada_nombre_trabajador)

        # Cargo del trabajador
        etiqueta_cargo_trabajador = QLabel("Cargo:")
        self.entrada_cargo_trabajador = QLineEdit()
        self.entrada_cargo_trabajador.setFont(QFont("Arial", 12))
        self.entrada_cargo_trabajador.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.layout_formulario.addRow(etiqueta_cargo_trabajador, self.entrada_cargo_trabajador)

        # Confirmación de condiciones
        etiqueta_confirmacion = QLabel("Confirmo que estoy en condiciones de hacer el trabajo")
        etiqueta_confirmacion.setFont(QFont("Arial", 12))
        self.combo_confirmacion = QComboBox()
        self.combo_confirmacion.addItems(["Seleccione", "Sí", "No"])
        self.combo_confirmacion.setFont(QFont("Arial", 12))
        self.combo_confirmacion.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.layout_formulario.addRow(etiqueta_confirmacion, self.combo_confirmacion)

        # Firma del trabajador
        etiqueta_firma_trabajador = QLabel("Firma:")
        self.entrada_firma_trabajador = QLineEdit()
        self.entrada_firma_trabajador.setFont(QFont("Arial", 12))
        self.entrada_firma_trabajador.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.layout_formulario.addRow(etiqueta_firma_trabajador, self.entrada_firma_trabajador)

    def crear_frame_botones(self):
        frame_botones = QHBoxLayout()
        frame_botones.setContentsMargins(0, 0, 0, 0)  # Ajustar márgenes para botones
        frame_botones.setSpacing(10)  # Espaciado entre botones
        self.layout_principal.addLayout(frame_botones)

        boton_enviar = QPushButton("Guardar Respuestas y Volver al Menú")
        boton_enviar.setFont(QFont("Arial", 14, QFont.Bold))
        boton_enviar.setStyleSheet("""
            QPushButton {
                padding: 12px;
                background-color: #3498db;  # Azul
                color: white;
                border-radius: 5px;
                font: bold 14pt;
            }
            QPushButton:hover {
                background-color: #2980b9;  # Azul oscuro
            }
        """)
        boton_enviar.clicked.connect(self.comprobar_respuestas_y_volver)
        frame_botones.addWidget(boton_enviar)
    
    def comprobar_respuestas_y_volver(self):
        """Verifica las respuestas antes de guardar y vuelve al menú principal."""
        nombre = self.entrada_nombre_trabajador.text().strip()
        cargo = self.entrada_cargo_trabajador.text().strip()
        confirmacion = self.combo_confirmacion.currentText()
        firma = self.entrada_firma_trabajador.text().strip()

        if not nombre or not cargo or confirmacion == "Seleccione" or not firma:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos antes de guardar.")
            return

        # Guardar respuestas en la base de datos
        paso = 5
        id_art = self.id_art
        numero_pregunta1 = "Nombre"
        numero_pregunta2 = "Cargo"
        numero_pregunta3 = "Confirma"
        numero_pregunta4 = "Firma"
        tipo_respuesta = 'trabajador'

        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta1, nombre)
        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta2, cargo)
        self.db.insertar_respuesta(id_art, tipo_respuesta, paso, numero_pregunta3, confirmacion)
        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta4, firma)
        self.db.art_en_espera(id_art)
        
        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Guardado Exitoso", "Las respuestas han sido guardadas correctamente.")
        self.abrir_formulario_paso5()

    def abrir_formulario_paso5(self):
        self.close()
        ventana = ControladorPasos.abrir_login()
        self.app = ventana
        self.app.show()
