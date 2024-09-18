from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QRadioButton, 
    QPushButton, QVBoxLayout, QFormLayout, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QFont
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD

class FormularioPaso5Supervisor(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.controladorARTSUP_BD = ControladorARTSUPconBD()
        self.setWindowTitle("Paso 5: Condiciones Físicas y Psicológicas para Realizar el Trabajo")
        self.setStyleSheet("background-color: #f0f0f0;")

        # Configuración de la ventana
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout()
        self.widget_central.setLayout(self.layout_principal)

        # Crear el título y los formularios
        self.crear_titulo()
        self.crear_combo_confirmacion()
        self.crear_frame_formulario()
        self.crear_frame_botones()

        self.showMaximized()

    def crear_titulo(self):
        """Crea y configura el título de la ventana."""
        etiqueta_titulo = QLabel("Paso 5: Condiciones Físicas y Psicológicas para Realizar el Trabajo / Validación ART por Equipo Ejecutor")
        etiqueta_titulo.setFont(QFont("Arial", 16, QFont.Bold))
        etiqueta_titulo.setStyleSheet("background-color: #003366; color: white; padding: 10px; margin-bottom: 10px;")
        self.layout_principal.addWidget(etiqueta_titulo)

    def crear_combo_confirmacion(self):
        """Crea un ComboBox para la selección de 'Confirmación Trabajador' o 'Confirmación Supervisor'."""
        self.combo_confirmacion = QComboBox()
        self.combo_confirmacion.addItems(["Confirmación Trabajador", "Confirmación Supervisor"])
        self.combo_confirmacion.setFont(QFont("Arial", 12))
        self.combo_confirmacion.currentIndexChanged.connect(self.cambiar_seccion_confirmacion)
        self.layout_principal.addWidget(self.combo_confirmacion)

    def crear_frame_formulario(self):
        """Crea y configura el formulario del paso 5."""
        self.frame_formulario = QWidget()
        self.layout_formulario = QFormLayout(self.frame_formulario)
        self.layout_formulario.setSpacing(20)  # Mayor espacio entre campos
        self.layout_formulario.setContentsMargins(50, 20, 50, 20)  # Márgenes ajustados
        self.layout_principal.addWidget(self.frame_formulario)

        # Crear campos del formulario
        self.crear_campos_formulario()

    def crear_campos_formulario(self):
        """Crea los campos del formulario para el paso 5."""
        self.crear_grupo_supervisores()

    def crear_grupo_supervisores(self):
        """Crea el grupo de campos relacionados con los supervisores."""
        # Título del grupo
        etiqueta_supervisores = QLabel("Información del Supervisor")
        etiqueta_supervisores.setFont(QFont("Arial", 14, QFont.Bold))
        self.layout_formulario.addRow(etiqueta_supervisores)

        # Nombre del supervisor
        etiqueta_nombre_supervisor = QLabel("Nombre:")
        self.entrada_nombre_supervisor = QLineEdit()
        self.entrada_nombre_supervisor.setFont(QFont("Arial", 12))
        self.entrada_nombre_supervisor.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ced4da;")
        self.layout_formulario.addRow(etiqueta_nombre_supervisor, self.entrada_nombre_supervisor)

        # Cargo del supervisor
        etiqueta_cargo_supervisor = QLabel("Cargo:")
        self.entrada_cargo_supervisor = QLineEdit()
        self.entrada_cargo_supervisor.setFont(QFont("Arial", 12))
        self.entrada_cargo_supervisor.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ced4da;")
        self.layout_formulario.addRow(etiqueta_cargo_supervisor, self.entrada_cargo_supervisor)

        # Confirmación de condiciones
        etiqueta_confirmacion = QLabel("¿Verifiqué las condiciones físicas y psicológicas de todo el Equipo Ejecutor del Trabajo?")
        etiqueta_confirmacion.setFont(QFont("Arial", 12))
        self.radio_si_confirmacion = QRadioButton("Sí")
        self.radio_no_confirmacion = QRadioButton("No")
        self.radio_si_confirmacion.setFont(QFont("Arial", 12))
        self.radio_no_confirmacion.setFont(QFont("Arial", 12))
        grupo_confirmacion = QHBoxLayout()
        grupo_confirmacion.addWidget(self.radio_si_confirmacion)
        grupo_confirmacion.addWidget(self.radio_no_confirmacion)
        self.layout_formulario.addRow(etiqueta_confirmacion, grupo_confirmacion)

        # Firma del supervisor
        etiqueta_firma_supervisor = QLabel("Firma:")
        self.entrada_firma_supervisor = QLineEdit()
        self.entrada_firma_supervisor.setFont(QFont("Arial", 12))
        self.entrada_firma_supervisor.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #ced4da;")
        self.layout_formulario.addRow(etiqueta_firma_supervisor, self.entrada_firma_supervisor)

    def crear_frame_botones(self):
        frame_botones = QHBoxLayout()
        frame_botones.setContentsMargins(50, 20, 50, 20)  # Márgenes para botones
        frame_botones.setSpacing(20)  # Espaciado entre botones
        self.layout_principal.addLayout(frame_botones)

        boton_enviar = QPushButton("Guardar Respuestas y Volver al Menú")
        boton_enviar.setFont(QFont("Arial", 12))
        boton_enviar.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border-radius: 5px;
                background-color: #e67e22;  # Naranja
                color: white;
            }
            QPushButton:hover {
                background-color: #d35400;  # Naranja oscuro
            }
        """)
        boton_enviar.clicked.connect(self.comprobar_respuestas_y_volver)
        frame_botones.addWidget(boton_enviar)

    def cambiar_seccion_confirmacion(self):
        """Cambia entre la visualización de 'Confirmación Trabajador' y 'Confirmación Supervisor'."""
        seleccion = self.combo_confirmacion.currentText()
        print(f"Sección seleccionada: {seleccion}")  # Depuración

        if seleccion == "Confirmación Trabajador":
            self.entrada_nombre_supervisor.setReadOnly(True)
            self.entrada_cargo_supervisor.setReadOnly(True)
            self.radio_si_confirmacion.setEnabled(False)
            self.radio_no_confirmacion.setEnabled(False)
            self.entrada_firma_supervisor.setReadOnly(True)

            # Cargar respuestas de trabajador de la base de datos
            respuestas_trabajador = self.controladorARTSUP_BD.obtener_respuesta_paso5(self.id_art)
            print(f"Respuestas del trabajador: {respuestas_trabajador}")  # Depuración

            self.entrada_nombre_supervisor.setText(respuestas_trabajador.get("nombre", ""))
            self.entrada_cargo_supervisor.setText(respuestas_trabajador.get("cargo", ""))
            self.radio_si_confirmacion.setChecked(respuestas_trabajador.get("confirmacion") == "Sí")
            self.radio_no_confirmacion.setChecked(respuestas_trabajador.get("confirmacion") == "No")
            self.entrada_firma_supervisor.setText(respuestas_trabajador.get("firma", ""))

        else:
            self.entrada_nombre_supervisor.setReadOnly(False)
            self.entrada_cargo_supervisor.setReadOnly(False)
            self.radio_si_confirmacion.setEnabled(True)
            self.radio_no_confirmacion.setEnabled(True)
            self.entrada_firma_supervisor.setReadOnly(False)

    def comprobar_respuestas_y_volver(self):
        """Verifica las respuestas antes de guardar y vuelve al menú principal."""
        nombre = self.entrada_nombre_supervisor.text().strip()
        cargo = self.entrada_cargo_supervisor.text().strip()
        confirmacion = self.radio_si_confirmacion.isChecked() or self.radio_no_confirmacion.isChecked()
        firma = self.entrada_firma_supervisor.text().strip()

        if not nombre or not cargo or not confirmacion or not firma:
            QMessageBox.warning(self, "Error", "Por favor, complete todos los campos antes de guardar.")
            return

        if self.radio_si_confirmacion.isChecked():
            reply = QMessageBox.question(
                self, 
                "Confirmación", 
                "Si confirmas que verificaste, estarás aprobando la ART. ¿Deseas continuar?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        respuesta_verificación = "Sí" if self.radio_si_confirmacion.isChecked() else "No"
        paso = 5
        id_art = self.id_art
        numero_pregunta1 = "Nombre"
        numero_pregunta2 = "Cargo"
        numero_pregunta3 = "Confirma"
        numero_pregunta4 = "Firma"
        tipo_respuesta = 'supervisor'

        # Guardar respuestas en la base de datos
        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta1, nombre)
        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta2, cargo)
        self.db.insertar_respuesta(id_art, tipo_respuesta, paso, numero_pregunta3, respuesta_verificación)
        self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, numero_pregunta4, firma)
        self.db.art_aprobada(id_art)
        
        # Mostrar mensaje de éxito
        QMessageBox.information(self, "Guardado Exitoso", "Las respuestas han sido guardadas correctamente.")
        
        self.abrir_menu_principal()

    def abrir_menu_principal(self):
        """Cierra la ventana actual y abre el menú principal."""
        self.close()
        ventana = ControladorPasos.abrir_login()
        self.app = ventana
        self.app.show()