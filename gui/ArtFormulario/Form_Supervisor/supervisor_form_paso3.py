from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, 
    QFormLayout, QPushButton, QHBoxLayout, QTextEdit
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD

class FormularioPaso3Supervisor(QMainWindow):  
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.controladorARTSUP_BD = ControladorARTSUPconBD()
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
        etiqueta_subtitulo = QLabel("Respuestas ART por el trabajador")
        etiqueta_subtitulo.setStyleSheet("font: 12pt 'Arial'; margin-bottom: 10px;")
        etiqueta_subtitulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(etiqueta_subtitulo)

        # Frame para el formulario
        layout_formulario = QFormLayout()
        layout_formulario.setLabelAlignment(Qt.AlignRight)
        layout_formulario.setSpacing(15)
        layout_principal.addLayout(layout_formulario)

        # Crear secciones de riesgos y medidas de control (solo visibles)
        self.crear_seccion_riesgos(layout_formulario)
        self.crear_seccion_medidas_control(layout_formulario)

        # Frame para botones
        frame_botones = QHBoxLayout()
        layout_principal.addLayout(frame_botones)

        # Botón para avanzar al formulario 4
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #e67e22; color: white; font: bold 14pt;")
        boton_siguiente.clicked.connect(self.abrir_formulario_paso4)
        frame_botones.addWidget(boton_siguiente)

        self.showMaximized()

    def crear_seccion_riesgos(self, layout_formulario):
        riesgos_trabajador = self.controladorARTSUP_BD.obtener_respuestas_riesgos(self.id_art, paso=3)  # Obtener las respuestas del trabajador
        for i in range(1, 8):
            etiqueta = QLabel(f"Riesgo {i}")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")
            texto_riesgo = QTextEdit()
            texto_riesgo.setStyleSheet("font: 12pt 'Arial';")
            texto_riesgo.setPlainText(riesgos_trabajador.get(f"riesgo_{i}", "No especificado"))
            texto_riesgo.setReadOnly(True)  
            layout_formulario.addRow(etiqueta, texto_riesgo)

    def crear_seccion_medidas_control(self, layout_formulario):
        medidas_control_trabajador = self.controladorARTSUP_BD.obtener_respuestas_medidas_control(self.id_art, paso=3)  # Obtener respuestas
        for i in range(1, 8):
            etiqueta = QLabel(f"Medida de Control {i}")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")
            texto_medida_control = QTextEdit()
            texto_medida_control.setStyleSheet("font: 12pt 'Arial';")
            texto_medida_control.setPlainText(medidas_control_trabajador.get(f"medida_control_{i}", "No especificado"))
            texto_medida_control.setReadOnly(True) 
            layout_formulario.addRow(etiqueta, texto_medida_control)

    def abrir_formulario_paso4(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso4(self.id_art)  
        self.app = ventana
        self.app.show()