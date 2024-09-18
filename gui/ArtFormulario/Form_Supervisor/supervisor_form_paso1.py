from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFormLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from Controladores.Controlador_ART_BD import ControladorARTconBD
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD
import datetime

class FormularioPaso1Supervisor(QMainWindow):
    def __init__(self, id_Art):
        super().__init__()

        self.id_Art = id_Art
        self.controlador = ControladorARTconBD()
        self.controladorARTSUP_BD = ControladorARTSUPconBD()
        self.setWindowTitle("Paso 1: Información del Trabajo")
        self.setGeometry(0, 0, 2000, 2000)  # Ajustar las dimensiones iniciales
        self.setStyleSheet("background-color: lightgrey; color: black; font: 14pt 'Arial';")

        layout = QVBoxLayout()

        # Título
        self.titulo = QLabel("Paso 1: Información del Trabajo")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font: bold 20pt; margin-bottom: 20px;")
        layout.addWidget(self.titulo)

        # Campos del formulario
        self.formulario_layout = QFormLayout()

        # Campo Supervisor que asigna el trabajo (Editable)
        self.supervisor_edit = QLineEdit()
        self.supervisor_edit.setPlaceholderText("Supervisor que asigna el trabajo")
        self.supervisor_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.formulario_layout.addRow(QLabel("Supervisor que asigna el trabajo:"), self.supervisor_edit)

        # Otros campos (Deshabilitados)
        self.empresa_edit = QLineEdit()
        self.empresa_edit.setPlaceholderText("Empresa")
        self.empresa_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.empresa_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Empresa:"), self.empresa_edit)

        self.gerencia_edit = QLineEdit()
        self.gerencia_edit.setPlaceholderText("Gerencia")
        self.gerencia_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.gerencia_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Gerencia:"), self.gerencia_edit)

        self.fecha_edit = QLineEdit()
        self.fecha_edit.setPlaceholderText("Fecha")
        self.fecha_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.fecha_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Fecha:"), self.fecha_edit)

        self.hora_inicio_edit = QLineEdit()
        self.hora_inicio_edit.setPlaceholderText("Hora Inicio")
        self.hora_inicio_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.hora_inicio_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Hora Inicio:"), self.hora_inicio_edit)

        self.hora_termino_edit = QLineEdit()
        self.hora_termino_edit.setPlaceholderText("Hora Término")
        self.hora_termino_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.hora_termino_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Hora Término:"), self.hora_termino_edit)

        self.superintendencia_edit = QLineEdit()
        self.superintendencia_edit.setPlaceholderText("Superintendencia/Dirección")
        self.superintendencia_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.superintendencia_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Superintendencia/Dirección:"), self.superintendencia_edit)

        self.trabajo_realizar_edit = QLineEdit()
        self.trabajo_realizar_edit.setPlaceholderText("Trabajo a Realizar")
        self.trabajo_realizar_edit.setStyleSheet("padding: 10px; border-radius: 5px;")
        self.trabajo_realizar_edit.setDisabled(True)  # Deshabilitado
        self.formulario_layout.addRow(QLabel("Trabajo a Realizar:"), self.trabajo_realizar_edit)

        layout.addLayout(self.formulario_layout)

        # Botón de Siguiente
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setStyleSheet("padding: 10px; border-radius: 5px; background-color: #e67e22; color: white;")
        self.boton_siguiente.clicked.connect(self.registrar_art)  # Actualizado para llamar a registrar_art
        layout.addWidget(self.boton_siguiente)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        # Cargar los datos de la ART
        self.cargar_datos_art()

    def cargar_datos_art(self):
        datos_art = self.controlador.obtener_datos_art(self.id_Art)

        if datos_art:
            self.supervisor_edit.setText(datos_art.get("supervisor", ""))
            self.empresa_edit.setText(datos_art.get("empresa", ""))
            self.gerencia_edit.setText(datos_art.get("gerencia", ""))
            self.fecha_edit.setText(self.formatear_fecha(datos_art.get("fecha", "")))
            self.hora_inicio_edit.setText(self.formatear_tiempo(datos_art.get("hora_inicio", "")))
            self.hora_termino_edit.setText(self.formatear_tiempo(datos_art.get("hora_termino", "")))
            self.superintendencia_edit.setText(datos_art.get("superintendencia", ""))
            self.trabajo_realizar_edit.setText(datos_art.get("trabajo_realizar", ""))
        else:
            QMessageBox.warning(self, "Error", "No se encontraron datos para la ART especificada.")

    def formatear_fecha(self, fecha):
        if isinstance(fecha, datetime.date):
            return fecha.strftime("%d/%m/%Y")
        return str(fecha)

    def formatear_tiempo(self, tiempo):
        if isinstance(tiempo, datetime.timedelta):
            return str(tiempo)
        return str(tiempo)

    def registrar_art(self):
        supervisor = self.supervisor_edit.text()
        if not supervisor:
            QMessageBox.warning(self, "Advertencia", "El campo de supervisor no puede estar vacío.")
            return
        self.controladorARTSUP_BD.actualizar_supervisor(self.id_Art, supervisor)
        # Proceder al siguiente paso
        self.abrir_formulario_paso2()

    def abrir_formulario_paso2(self):
        id_Art = self.id_Art
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso2(id_Art)
        self.app = ventana
        self.app.show()
