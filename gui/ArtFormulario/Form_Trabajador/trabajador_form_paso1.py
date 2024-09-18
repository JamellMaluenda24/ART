from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QVBoxLayout, 
    QPushButton, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD
import re
from datetime import datetime

class FormularioPaso1Trabajador(QMainWindow):
    def __init__(self, rut):
        super().__init__()
        self.setWindowTitle("ART - Paso 1: Información del Trabajo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")

        self.controlador_bd = ControladorARTconBD()
        self.rut = rut
        self.id_art = None 
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título
        self.titulo = QLabel("Paso 1: Información del Trabajo")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font: bold 22pt; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(self.titulo)

        # Campos del formulario
        self.formulario_layout = QFormLayout()
        self.formulario_layout.setLabelAlignment(Qt.AlignRight)
        self.formulario_layout.setSpacing(15)

        # Campo Supervisor
        self.supervisor_edit = QLineEdit()
        self.supervisor_edit.setPlaceholderText("Supervisor que asigna el trabajo (Este campo será llenado por el supervisor)")
        self.supervisor_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.supervisor_edit.setDisabled(True)
        self.formulario_layout.addRow(QLabel("Supervisor:"), self.supervisor_edit)

        # Campo Empresa
        self.empresa_edit = QLineEdit()
        self.empresa_edit.setPlaceholderText("Empresa (Ejemplo: MiEmpresa S.A.)")
        self.empresa_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Empresa:"), self.empresa_edit)

        # Campo Gerencia
        self.gerencia_edit = QLineEdit()
        self.gerencia_edit.setPlaceholderText("Gerencia (Ejemplo: Gerencia de Operaciones)")
        self.gerencia_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Gerencia:"), self.gerencia_edit)

        # Campo Fecha
        self.fecha_edit = QLineEdit()
        self.fecha_edit.setPlaceholderText("Fecha (YYYY-MM-DD, Ejemplo: 2024-08-30)")
        self.fecha_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Fecha:"), self.fecha_edit)

        # Campo Hora Inicio
        self.hora_inicio_edit = QLineEdit()
        self.hora_inicio_edit.setPlaceholderText("Hora Inicio (HH:MM:SS, Ejemplo: 09:00:00)")
        self.hora_inicio_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Hora Inicio:"), self.hora_inicio_edit)

        # Campo Hora Término
        self.hora_termino_edit = QLineEdit()
        self.hora_termino_edit.setPlaceholderText("Hora Término (HH:MM:SS, Ejemplo: 18:00:00)")
        self.hora_termino_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Hora Término:"), self.hora_termino_edit)

        # Campo Superintendencia
        self.superintendencia_edit = QLineEdit()
        self.superintendencia_edit.setPlaceholderText("Superintendencia/Dirección (Ejemplo: Superintendencia Técnica)")
        self.superintendencia_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Superintendencia/Dirección:"), self.superintendencia_edit)

        # Campo Trabajo a Realizar
        self.trabajo_realizar_edit = QLineEdit()
        self.trabajo_realizar_edit.setPlaceholderText("Trabajo a Realizar (Ejemplo: Mantenimiento preventivo)")
        self.trabajo_realizar_edit.setStyleSheet("padding: 10px; border-radius: 5px; border: 1px solid #bdc3c7;")
        self.formulario_layout.addRow(QLabel("Trabajo a Realizar:"), self.trabajo_realizar_edit)

        layout.addLayout(self.formulario_layout)

        # Botón de Siguiente
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #3498db; color: white; font: bold 14pt;")
        self.boton_siguiente.clicked.connect(self.registrar_art)
        layout.addWidget(self.boton_siguiente)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
        self.showMaximized()

    def registrar_art(self):
        empresa = self.empresa_edit.text()
        gerencia = self.gerencia_edit.text()
        fecha = self.fecha_edit.text()
        hora_inicio = self.hora_inicio_edit.text()
        hora_termino = self.hora_termino_edit.text()
        superintendencia = self.superintendencia_edit.text()
        trabajo_realizar = self.trabajo_realizar_edit.text()

        if not all([empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar]):
            QMessageBox.warning(self, "Error", "Por favor complete todos los campos.")
            return

        if not self.validar_fecha(fecha):
            QMessageBox.warning(self, "Error", "La fecha no es válida. Use el formato YYYY-MM-DD y asegúrese de que el año no sea menor a 2024.")
            return

        if not self.validar_hora(hora_inicio) or not self.validar_hora(hora_termino):
            QMessageBox.warning(self, "Error", "La hora no es válida. Use el formato HH:MM:SS y asegúrese de que las horas no superen 24, y los minutos y segundos no superen 60.")
            return

        try:
            self.id_art = self.controlador_bd.guardar_art(self.rut, empresa, gerencia, fecha, hora_inicio, hora_termino, superintendencia, trabajo_realizar)
            if self.id_art:
                QMessageBox.information(self, "Éxito", f"Datos guardados exitosamente. ID de ART: {self.id_art}")
                self.abrir_formulario_paso2()
            else:
                QMessageBox.warning(self, "Error", "No se pudo registrar el formulario ART.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo registrar el formulario ART. Error: {e}")

    def validar_fecha(self, fecha):
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            if fecha_obj.year < 2024:
                return False
            return True
        except ValueError:
            return False

    def validar_hora(self, hora):
        if re.match(r"^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$", hora):
            return True
        return False

    def abrir_formulario_paso2(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso2(self.id_art) 
        self.app = ventana
        ventana.show()
