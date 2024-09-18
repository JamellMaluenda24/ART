from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, 
    QFormLayout, QPushButton, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD

class FormularioPaso4Supervisor(QMainWindow):  
    def __init__(self, id_art):
        super().__init__()

        # Inicialización de atributos
        self.id_art = id_art
        self.controladorARTSUP_BD = ControladorARTSUPconBD()

        # Configuración de la ventana principal
        self.setWindowTitle("ART - Paso 4: Trabajos en Simultáneo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")

        # Crear el widget central
        contenedor = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Título
        etiqueta_titulo = QLabel(f"Paso 4: Trabajos en Simultáneo (ART ID: {self.id_art})")
        etiqueta_titulo.setFont(QFont("Arial", 20, QFont.Bold))
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        layout_principal.addWidget(etiqueta_titulo)

        # Subtítulo
        etiqueta_subtitulo = QLabel("Respuestas del trabajador sobre trabajo simultáneo")
        etiqueta_subtitulo.setFont(QFont("Arial", 12))
        etiqueta_subtitulo.setAlignment(Qt.AlignCenter)
        etiqueta_subtitulo.setStyleSheet("margin-bottom: 10px;")
        layout_principal.addWidget(etiqueta_subtitulo)

        # Frame para el formulario
        self.layout_formulario = QFormLayout()
        self.layout_formulario.setLabelAlignment(Qt.AlignRight)
        self.layout_formulario.setSpacing(15)
        layout_principal.addLayout(self.layout_formulario)

        # Crear las respuestas del trabajador
        self.crear_seccion_respuestas_paso4()

        # Frame para botones
        frame_botones = QHBoxLayout()
        layout_principal.addLayout(frame_botones)

        # Botón para avanzar al siguiente paso
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setFont(QFont("Arial", 14, QFont.Bold))
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #e67e22; color: white;")
        boton_siguiente.clicked.connect(self.abrir_formulario_paso5)
        frame_botones.addWidget(boton_siguiente)

        self.showMaximized()

    def crear_seccion_respuestas_paso4(self):
        """Crea las respuestas del trabajador en el formulario."""        
        # Definir preguntas y códigos
        preguntas = [
            ("¿Existen trabajos en simultáneo?", "TRA-07"),   
            ("¿Se realizó la coordinación con el líder de la cuadrilla que realiza el trabajo en simultáneo?", "TRA-08"),
            ("¿Se realizó la verificación cruzada de Controles Críticos?", "TRA-09"),
            ("¿Se comunicó a todos los trabajadores las acciones de control que debe aplicar en trabajos simultáneos?", "TRA-10"),
            ("Describa el contexto del trabajo en simultáneo y verifique(Solo si aplica):", "trabajo simultaneo")
        ]
        
        respuestas_trabajador = self.controladorARTSUP_BD.obtener_respuesta_paso4(self.id_art, paso=4)
        respuesta_trabajo_simultaneo = self.controladorARTSUP_BD.obtener_respuesta_paso4_TS(self.id_art, paso=4).get('trabajo simultaneo', 'No especificado')
        
        for pregunta, codigo in preguntas:
            etiqueta = QLabel(pregunta)
            etiqueta.setFont(QFont("Arial", 14))
            etiqueta.setStyleSheet("margin-bottom: 10px;")
            texto_respuesta = QTextEdit()
            texto_respuesta.setFont(QFont("Arial", 12))
            
            # Obtener la respuesta correspondiente
            if codigo == "trabajo simultaneo":
                respuesta = respuesta_trabajo_simultaneo
            else:
                respuesta = respuestas_trabajador.get(codigo, "No especificado")
            
            if respuesta == 'Si':
                respuesta = "Sí"
            elif respuesta == 'No':
                respuesta = "No"
            
            texto_respuesta.setPlainText(respuesta)
            texto_respuesta.setReadOnly(True)
            self.layout_formulario.addRow(etiqueta, texto_respuesta)

    def abrir_formulario_paso5(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso5(self.id_art)
        self.app = ventana
        self.app.show()
