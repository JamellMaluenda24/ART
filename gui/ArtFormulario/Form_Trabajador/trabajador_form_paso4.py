from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QRadioButton, 
    QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QGroupBox, 
    QButtonGroup, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD

class FormularioPaso4Trabajador(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        
        # Inicialización de atributos
        self.id_art = id_art
        self.db = ControladorARTconBD()
        
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

        # Frame para el formulario
        self.layout_formulario = QFormLayout()
        self.layout_formulario.setLabelAlignment(Qt.AlignRight)
        self.layout_formulario.setSpacing(15)
        layout_principal.addLayout(self.layout_formulario)

        # Crear las preguntas y campos del formulario
        self.crear_preguntas_formulario()

        # Frame para botones
        frame_botones = QHBoxLayout()
        layout_principal.addLayout(frame_botones)

        # Botón para avanzar al siguiente formulario
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setFont(QFont("Arial", 14, QFont.Bold))
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #e67e22; color: white;")
        boton_siguiente.clicked.connect(self.comprobar_respuestas)
        frame_botones.addWidget(boton_siguiente)

        self.showMaximized()

    def crear_preguntas_formulario(self):
        """Crea las preguntas y los campos correspondientes en el formulario."""
        preguntas = [
            ("¿Existen trabajos en simultáneo?", "TRA-07"),  
            ("Si su respuesta es Sí, describa el contexto del trabajo en simultáneo y verifique:", "trabajo simultaneo"), 
            ("¿Se realizó la coordinación con el líder de la cuadrilla que realiza el trabajo en simultáneo?", "TRA-08"),
            ("¿Se realizó la verificación cruzada de Controles Críticos?", "TRA-09"),
            ("¿Se comunicó a todos los trabajadores las acciones de control que debe aplicar en trabajos simultáneos?", "TRA-10")
        ]

        self.variables_preguntas = []
        self.cuadros_texto = []

        # Crear cada pregunta del formulario
        for pregunta, codigo in preguntas:
            if codigo == "trabajo simultaneo":
                self.crear_cuadro_texto(pregunta, codigo)
            else:
                self.crear_grupo_radio(pregunta, codigo)

    def crear_grupo_radio(self, pregunta, codigo):
        """Crea un grupo de botones de radio para una pregunta específica."""
        etiqueta = QLabel(pregunta)
        etiqueta.setFont(QFont("Arial", 14))
        etiqueta.setStyleSheet("margin-bottom: 10px;")

        grupo_botones = QGroupBox()
        layout_botones = QHBoxLayout(grupo_botones)

        variable = QButtonGroup()
        self.variables_preguntas.append((variable, codigo))

        boton_si = QRadioButton("Sí")
        boton_no = QRadioButton("No")

        layout_botones.addWidget(boton_si)
        layout_botones.addWidget(boton_no)

        variable.addButton(boton_si)
        variable.addButton(boton_no)

        self.layout_formulario.addRow(etiqueta, grupo_botones)

    def crear_cuadro_texto(self, pregunta, codigo):
        """Crea un cuadro de texto para una pregunta específica."""
        etiqueta = QLabel(pregunta)
        etiqueta.setFont(QFont("Arial", 14))
        etiqueta.setStyleSheet("margin-bottom: 10px;")

        cuadro_texto = QTextEdit()
        cuadro_texto.setFont(QFont("Arial", 12))
        cuadro_texto.setStyleSheet("padding: 5px;")

        self.layout_formulario.addRow(etiqueta, cuadro_texto)
        self.cuadros_texto.append((cuadro_texto, codigo))

    def comprobar_respuestas(self):
        respuesta_trabajo_simultaneo = None
        for variable, codigo in self.variables_preguntas:
            respuesta = variable.checkedButton().text() if variable.checkedButton() else None
            if codigo == "TRA-07":
                respuesta_trabajo_simultaneo = respuesta
            elif respuesta is not None:
                self.db.insertar_respuesta(self.id_art, 'trabajador', 4, codigo, respuesta)
        
        # Verificar si se respondió la pregunta de trabajos simultáneos
        if respuesta_trabajo_simultaneo is None:
            QMessageBox.warning(self, "Error", "Por favor responda la pregunta sobre trabajos simultáneos antes de continuar.")
            return

        # Si la respuesta es Sí, verificar el contexto del trabajo simultáneo
        if respuesta_trabajo_simultaneo == "Sí":
            for cuadro_texto, codigo in self.cuadros_texto:
                respuesta_texto = cuadro_texto.toPlainText().strip()
                if codigo == "trabajo simultaneo" and respuesta_texto:
                    self.db.insertar_respuesta_texto(self.id_art, 'trabajador', 4, "trabajo simultaneo", respuesta_texto)
                elif codigo == "trabajo simultaneo" and not respuesta_texto:
                    QMessageBox.warning(self, "Error", "Por favor proporcione una descripción del contexto si la respuesta es Sí.")
                    return

        # Si la respuesta es No, insertar automáticamente "no hay trabajos simultáneos"
        elif respuesta_trabajo_simultaneo == "No":
            self.db.insertar_respuesta_texto(self.id_art, 'trabajador', 4, "trabajo simultaneo", "no hay trabajos simultáneos")

        # Guardar la respuesta de TRA-07 (Trabajo simultáneo)
        self.db.insertar_respuesta(self.id_art, 'trabajador', 4, "TRA-07", respuesta_trabajo_simultaneo)

        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_paso5(self.id_art)

    def abrir_formulario_paso5(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso5(id_art)
        self.app = ventana
        self.app.show()
