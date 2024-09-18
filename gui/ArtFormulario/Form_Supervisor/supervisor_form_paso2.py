from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QRadioButton, 
    QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QGroupBox, 
    QButtonGroup, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD

class FormularioPaso2Supervisor(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.dbART_SUP = ControladorARTSUPconBD()
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
        etiqueta_titulo = QLabel(f"ART - Paso 2: Verificación del Trabajo (ART ID: {self.id_art})")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setStyleSheet("font: bold 22pt; color: #2c3e50; margin-bottom: 20px;")
        layout_principal.addWidget(etiqueta_titulo)

        # Selector de tipo de preguntas
        self.combo_tipo_preguntas = QComboBox()
        self.combo_tipo_preguntas.addItem("Selecciona el Tipo de Pregunta")
        self.combo_tipo_preguntas.addItem("Preguntas del Supervisor")
        self.combo_tipo_preguntas.addItem("Preguntas del Trabajador")
        self.combo_tipo_preguntas.currentIndexChanged.connect(self.mostrar_preguntas)
        layout_principal.addWidget(self.combo_tipo_preguntas)

        # Frame para el formulario
        self.layout_formulario = QFormLayout()
        self.layout_formulario.setLabelAlignment(Qt.AlignRight)
        self.layout_formulario.setSpacing(15)
        layout_principal.addLayout(self.layout_formulario)

        # Frame para botones
        frame_botones = QHBoxLayout()

        # Botón para avanzar al siguiente formulario
        boton_siguiente = QPushButton("Siguiente Formulario")
        boton_siguiente.setStyleSheet("padding: 12px; border-radius: 5px; background-color: #3498db; color: white; font: bold 14pt;")
        boton_siguiente.clicked.connect(self.comprobar_respuestas)
        frame_botones.addWidget(boton_siguiente)

        layout_principal.addLayout(frame_botones)

        self.showMaximized()

    def mostrar_preguntas(self, index):
        # Limpiar el formulario actual
        while self.layout_formulario.count():
            child = self.layout_formulario.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        tipo_pregunta = self.combo_tipo_preguntas.currentIndex()
        if tipo_pregunta == 0:
            return  # No mostrar preguntas si no se ha seleccionado tipo

        preguntas = self.obtener_preguntas(tipo_pregunta)
        if preguntas:
            self.crear_seccion_preguntas(preguntas, tipo_pregunta)

    def obtener_preguntas(self, tipo_pregunta):
        # Aquí defines las preguntas según el tipo
        preguntas = []
        if tipo_pregunta == 1:  # Supervisor
            preguntas = [
                {"codigo": "SUP-01", "pregunta": "¿El trabajo que asignaré cuenta con un estándar, procedimiento y/o instructivo?"},
                {"codigo": "SUP-02", "pregunta": "¿El personal que asignaré para realizar el trabajo, cuenta con las capacitaciones, competencias, salud compatible y/o acreditaciones requeridas?"},
                {"codigo": "SUP-03", "pregunta": "¿Durante la planificación del trabajo, me aseguro de solicitar los permisos para ingresar a las áreas, intervenir equipos y/o interactuar con energías?"},
                {"codigo": "SUP-04", "pregunta": "¿Verifiqué que el personal cuenta con los elementos requeridos para realizar la segregación y señalización del área de trabajo, según diseño?"},
                {"codigo": "SUP-05", "pregunta": "¿El personal a mi cargo cuenta con sistema de comunicación de acuerdo al protocolo de emergencia del área?"},
                {"codigo": "SUP-06", "pregunta": "¿El personal que asignaré para realizar el trabajo, cuenta con los EPP definidos en el procedimiento de trabajo?"}
            ]
        elif tipo_pregunta == 2:  # Trabajador
            preguntas = [
                {"codigo": "TRA-01", "pregunta": "¿Conozco el estándar, procedimiento y/o instructivo del trabajo que ejecutaré? "},
                {"codigo": "TRA-02", "pregunta": "¿Cuento con las competencias y salud compatible para ejecutar el trabajo?"},
                {"codigo": "TRA-03", "pregunta": "¿Cuento con la autorización para ingresar al área a ejecutar el trabajo?"},
                {"codigo": "TRA-04", "pregunta": "¿Segregué y señalicé el área de trabajo con los elementos según diseño?"},
                {"codigo": "TRA-05", "pregunta": "¿Conozco el número de teléfono o frecuencia radial para dar aviso en caso de emergencia, según protocolo del área?"},
                {"codigo": "TRA-06", "pregunta": "¿Uso los EPP definidos para el trabajo y se encuentran en buenas condiciones?"}
            ]
        return preguntas

    def crear_seccion_preguntas(self, preguntas, tipo_pregunta):
        self.variables_trabajador = []
        self.variables_supervisor = []
        id_art = self.id_art

        if tipo_pregunta == 1:  # Supervisor
            # Solo muestra las preguntas del supervisor sin cargar respuestas
            for pregunta in preguntas:
                etiqueta = QLabel(f"Cód: {pregunta['codigo']} - {pregunta['pregunta']}")
                etiqueta.setStyleSheet("font: 12pt 'Arial';")

                grupo_botones = QGroupBox()
                layout_botones = QHBoxLayout()
                grupo_botones.setLayout(layout_botones)

                variable = QButtonGroup()
                self.variables_supervisor.append((pregunta["codigo"], variable))

                boton_si = QRadioButton("Sí")
                boton_no = QRadioButton("No")
                layout_botones.addWidget(boton_si)
                layout_botones.addWidget(boton_no)

                variable.addButton(boton_si)
                variable.addButton(boton_no)

                self.layout_formulario.addRow(etiqueta, grupo_botones)
        
        elif tipo_pregunta == 2:  # Trabajador
            # Carga las respuestas para el trabajador
            respuestas_trabajador = self.dbART_SUP.cargar_respuestas_art(id_art, 2)
            print(f"Respuestas Trabajador: {respuestas_trabajador}")  # Imprimir respuestas para depuración

            for pregunta in preguntas:
                etiqueta = QLabel(f"Cód: {pregunta['codigo']} - {pregunta['pregunta']}")
                etiqueta.setStyleSheet("font: 12pt 'Arial';")

                respuesta = respuestas_trabajador.get(pregunta["codigo"], "No Respondido")
                respuesta_label = QLabel(f"Respuesta: {respuesta}")
                respuesta_label.setStyleSheet("font: 12pt 'Arial'; color: #7f8c8d;")

                # Mostrar la pregunta y la respuesta
                self.layout_formulario.addRow(etiqueta, respuesta_label)

                # Asegurarse de que las respuestas del trabajador no sean editables
                respuesta_label.setDisabled(True)

    def comprobar_respuestas(self):
        respuestas_supervisor = [
            (codigo, grupo.checkedButton().text()) if grupo.checkedButton() else (codigo, None)
            for codigo, grupo in self.variables_supervisor
        ]
        if any(respuesta is None for _, respuesta in respuestas_supervisor):
            QMessageBox.warning(self, "Error", "Por favor responda todas las preguntas del supervisor antes de continuar.")
            return

        for codigo, respuesta in respuestas_supervisor:
            print(f"Código: {codigo}, Respuesta: {respuesta}")
            paso = 2
            tipo_respuesta = 'supervisor'
            self.db.insertar_respuesta_texto(self.id_art, tipo_respuesta, paso, codigo, respuesta)

        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_supervisor_paso2RC(self.id_art)

    def abrir_formulario_supervisor_paso2RC(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso2RC(id_art)
        self.app = ventana
        self.app.show()