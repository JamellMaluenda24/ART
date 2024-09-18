from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QRadioButton, 
    QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QGroupBox, QButtonGroup, QMessageBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  

class FormularioPaso2Trabajador(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.setWindowTitle("ART - Paso 2: Verificación del Trabajo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")

        # Crear el widget central
        contenedor = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Título
        etiqueta_titulo = QLabel(f"Paso 2: Verificación del Trabajo (ART ID: {self.id_art})")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setStyleSheet("font: bold 22pt; color: #2c3e50; margin-bottom: 20px;")
        layout_principal.addWidget(etiqueta_titulo)

        # Frame para el formulario
        layout_formulario = QFormLayout()
        layout_formulario.setLabelAlignment(Qt.AlignRight)
        layout_formulario.setSpacing(15)

        # Crear secciones de preguntas
        self.crear_preguntas_trabajador(layout_formulario)
        layout_principal.addLayout(layout_formulario)

        # Frame para botones
        frame_botones = QHBoxLayout()

        # Botón para avanzar al formulario 3
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #3498db; color: white; font: bold 14pt;")
        boton_siguiente.clicked.connect(self.comprobar_respuestas)
        frame_botones.addWidget(boton_siguiente)

        layout_principal.addLayout(frame_botones)

        self.showMaximized()

    def crear_preguntas_trabajador(self, layout_formulario):
        preguntas = [
            {"codigo": "TRA-01", "texto": "¿Conozco el estándar, procedimiento y/o instructivo del trabajo que ejecutaré?"},
            {"codigo": "TRA-02", "texto": "¿Cuento con las competencias y salud compatible para ejecutar el trabajo?"},
            {"codigo": "TRA-03", "texto": "¿Cuento con la autorización para ingresar al área a ejecutar el trabajo?"},
            {"codigo": "TRA-04", "texto": "¿Segregué y señalicé el área de trabajo con los elementos según diseño?"},
            {"codigo": "TRA-05", "texto": "¿Conozco el número de teléfono o frecuencia radial para dar aviso en caso de emergencia, según protocolo del área?"},
            {"codigo": "TRA-06", "texto": "¿Uso los EPP definidos para el trabajo y se encuentran en buenas condiciones?"}
        ]

        self.variables_trabajador = []

        for pregunta in preguntas:
            codigo = pregunta["codigo"]
            texto = pregunta["texto"]

            etiqueta = QLabel(texto)
            etiqueta.setStyleSheet("font: 12pt 'Arial';")

            grupo_botones = QGroupBox()
            layout_botones = QHBoxLayout()
            grupo_botones.setLayout(layout_botones)

            variable = QButtonGroup()
            self.variables_trabajador.append((codigo, variable))

            boton_si = QRadioButton("Sí")
            boton_no = QRadioButton("No")
            layout_botones.addWidget(boton_si)
            layout_botones.addWidget(boton_no)

            variable.addButton(boton_si)
            variable.addButton(boton_no)

            layout_formulario.addRow(etiqueta, grupo_botones)

    def comprobar_respuestas(self):
        respuestas = [(codigo, grupo.checkedButton().text() if grupo.checkedButton() else None) for codigo, grupo in self.variables_trabajador]
        if any(respuesta is None for _, respuesta in respuestas):
            QMessageBox.warning(self, "Error", "Por favor responda todas las preguntas antes de continuar.")
            return

        for codigo, respuesta in respuestas:
            paso = 2
            tipo_respuesta = 'trabajador'  # Establecer el tipo de respuesta como 'trabajador'
            id_art = self.id_art
            self.db.insertar_respuesta(id_art, tipo_respuesta, paso, codigo, respuesta)
        
        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_paso2RC()   

    def abrir_formulario_paso2RC(self):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso2RC(self.id_art)
        self.app = ventana
        self.app.show()
