from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, 
    QFormLayout, QPushButton, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  

class FormularioPaso3Trabajador(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.setWindowTitle("ART - Paso 3: Riesgos Críticos Específicos del Trabajo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")

        # Crear el widget central
        contenedor = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Título
        etiqueta_titulo = QLabel(f"Paso 3: Riesgos Críticos Específicos del Trabajo (ART ID: {self.id_art})")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setStyleSheet("font: bold 22pt; color: #2c3e50; margin-bottom: 20px;")
        layout_principal.addWidget(etiqueta_titulo)

        # Subtítulo
        etiqueta_subtitulo = QLabel("Ingrese los riesgos y medidas de control relacionados con el trabajo.")
        etiqueta_subtitulo.setStyleSheet("font: 12pt 'Arial'; margin-bottom: 10px;")
        etiqueta_subtitulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(etiqueta_subtitulo)

        # Frame para el formulario
        layout_formulario = QFormLayout()
        layout_formulario.setLabelAlignment(Qt.AlignRight)
        layout_formulario.setSpacing(15)
        layout_principal.addLayout(layout_formulario)

        # Crear secciones de riesgos y medidas de control
        self.crear_seccion_riesgos(layout_formulario)
        self.crear_seccion_medidas_control(layout_formulario)

        # Frame para botones
        frame_botones = QHBoxLayout()
        layout_principal.addLayout(frame_botones)

        # Botón para avanzar al formulario 4
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #e67e22; color: white; font: bold 14pt;")
        boton_siguiente.clicked.connect(self.comprobar_respuestas)
        frame_botones.addWidget(boton_siguiente)

        self.showMaximized()

    def crear_seccion_riesgos(self, layout_formulario):
        self.text_riesgos = []
        for i in range(1, 8):
            etiqueta = QLabel(f"Riesgo {i}")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")
            texto_riesgo = QTextEdit()
            texto_riesgo.setStyleSheet("font: 12pt 'Arial';")
            texto_riesgo.setPlaceholderText(f"Ingrese Riesgo {i} aquí...")
            self.text_riesgos.append(texto_riesgo)
            layout_formulario.addRow(etiqueta, texto_riesgo)

    def crear_seccion_medidas_control(self, layout_formulario):
        self.text_medidas_control = []
        for i in range(1, 8):
            etiqueta = QLabel(f"Medida de Control {i}")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")
            texto_medida_control = QTextEdit()
            texto_medida_control.setStyleSheet("font: 12pt 'Arial';")
            texto_medida_control.setPlaceholderText(f"Ingrese Medida de Control {i} aquí...")
            self.text_medidas_control.append(texto_medida_control)
            layout_formulario.addRow(etiqueta, texto_medida_control)

    def comprobar_respuestas(self):
        riesgos = [texto_riesgo.toPlainText().strip() for texto_riesgo in self.text_riesgos]
        medidas_control = [texto_medida_control.toPlainText().strip() for texto_medida_control in self.text_medidas_control]
        paso = 3 
        id_art = self.id_art
        tipo_respuesta = 'trabajador'

        if not any(riesgos) and not any(medidas_control):
            QMessageBox.warning(self, "Error", "Por favor ingrese al menos un riesgo y una medida de control antes de continuar.")
            return
        
        # Guardar riesgos en la base de datos
        for numero_riesgo, riesgo in enumerate(riesgos, start=1):
            if riesgo:
                self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, f"riesgo_{numero_riesgo}", riesgo)
            else:
                self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, f"riesgo_{numero_riesgo}", "no")

        # Guardar medidas de control en la base de datos
        for numero_medida, medida in enumerate(medidas_control, start=1):
            if medida:
                self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, f"medida_control_{numero_medida}", medida)
            else:
                self.db.insertar_respuesta_texto(id_art, tipo_respuesta, paso, f"medida_control_{numero_medida}", "no")

        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_paso4(self.id_art)

    def abrir_formulario_paso4(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso4(id_art)
        self.app = ventana
        self.app.show()
