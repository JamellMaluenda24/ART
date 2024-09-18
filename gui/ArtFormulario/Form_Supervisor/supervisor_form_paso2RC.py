from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QRadioButton,
    QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QGroupBox,
    QButtonGroup, QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  
from Controladores.Controlador_ARTSUP_BD import ControladorARTSUPconBD
from Controladores.Preguntas.preguntas_riesgos_criticos import obtener_preguntas_sup_por_codigo, obtener_preguntas_tr_por_codigo

class FormularioPaso2SupervisorRC(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
        self.dbART_SUP = ControladorARTSUPconBD()
        self.setWindowTitle("ART - Paso 2: Riesgos Críticos Específicos del Trabajo")
        self.setStyleSheet("background-color: #f2f2f2; color: #333; font: 14pt 'Arial';")

        # Crear el widget central
        contenedor = QWidget()
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(20, 20, 20, 20)
        layout_principal.setSpacing(10)
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Título
        etiqueta_titulo = QLabel(f"Riesgos Críticos Específicos del Trabajo (ART ID: {self.id_art})")
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

        if index == 0:
            return  # No mostrar preguntas si no se ha seleccionado tipo

        # Cargar preguntas según el tipo seleccionado
        preguntas = self.obtener_preguntas(index)
        if preguntas:
            self.crear_seccion_preguntas(preguntas, index)
        else:
            etiqueta = QLabel("No se encontraron preguntas para el tipo seleccionado.")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")
            self.layout_formulario.addRow(etiqueta)

    def obtener_preguntas(self, tipo_pregunta):
        preguntas = []
        id_art = self.id_art
        paso = 2
        codigo_rc = self.dbART_SUP.obtener_codigo_rc(id_art, paso)
        print(f"Código RC obtenido: {codigo_rc}")  # Agregar impresión para depuración
        if tipo_pregunta == 1:  # Supervisor
            if codigo_rc:
                preguntas = self.obtener_preguntas_supervisor(codigo_rc)
        elif tipo_pregunta == 2:  # Trabajador
            if codigo_rc:
                preguntas = obtener_preguntas_tr_por_codigo(codigo_rc)
        return preguntas

    def obtener_preguntas_supervisor(self, codigo_rc):
        return obtener_preguntas_sup_por_codigo(codigo_rc)

    def crear_seccion_preguntas(self, preguntas, tipo_pregunta):
        self.variables_trabajador = []
        self.variables_supervisor = []
        id_art = self.id_art

        if tipo_pregunta == 1:  # Supervisor
            # Muestra las preguntas del supervisor
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
                respuestas_trabajador = self.dbART_SUP.cargar_respuestas_artRC(id_art, 2)
                print(f"Respuestas Trabajador: {respuestas_trabajador}")  # Imprimir respuestas para depuración

                for pregunta in preguntas:
                    etiqueta = QLabel(f"Cód: {pregunta['codigo']} - {pregunta['pregunta']}")
                    etiqueta.setStyleSheet("font: 12pt 'Arial';")

                    respuesta = respuestas_trabajador.get(pregunta["codigo"], "No Respondido")
                    print(f"Pregunta: {pregunta['codigo']}, Respuesta: {respuesta}")  # Imprimir para depuración

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
            paso = 2
            tipo_respuesta = 'supervisor'
            self.db.insertar_respuesta_texto(self.id_art, tipo_respuesta, paso, codigo, respuesta)

        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_supervisor_paso3(self.id_art)

    def abrir_formulario_supervisor_paso3(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso3(id_art)
        self.app = ventana
        self.app.show()
