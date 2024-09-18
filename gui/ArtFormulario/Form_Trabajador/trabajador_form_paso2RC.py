from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QRadioButton, 
    QVBoxLayout, QFormLayout, QPushButton, QHBoxLayout, QGroupBox, QButtonGroup, 
    QMessageBox, QComboBox
)
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_ART_BD import ControladorARTconBD  

class FormularioPaso2TrabajadorRC(QMainWindow):
    def __init__(self, id_art):
        super().__init__()
        self.id_art = id_art
        self.db = ControladorARTconBD()
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

        # Selección de Riesgo Crítico
        self.combo_riesgos = QComboBox()
        self.combo_riesgos.addItem("Selecciona un Riesgo Crítico")
        self.combo_riesgos.addItem("RC01 - Contacto con energía eléctrica")
        self.combo_riesgos.addItem("RC02 - Caída de distinto nivel")
        self.combo_riesgos.addItem("RC03 - Aplastamiento / Atrapamiento por carga suspendida")
        self.combo_riesgos.addItem("RC04 - Proyección descontrolada de líquidos a alta presión")
        self.combo_riesgos.addItem("RC05 - Caída de roca a cielo abierto")
        self.combo_riesgos.addItem("RC06 - Incendio")
        self.combo_riesgos.addItem("RC07 - Contacto con sustancias químicas peligrosas")
        self.combo_riesgos.addItem("RC09 - Atrapamiento / Aprisionamiento con partes móviles")
        self.combo_riesgos.addItem("RC10 - Choque / Colisión / Volcamiento de vehículo")
        self.combo_riesgos.addItem("RC11 - Exposición a atmósferas peligrosas en espacios confinados")
        self.combo_riesgos.addItem("RC12 - Contacto con material fundido")
        self.combo_riesgos.addItem("RC13 - Caída de objetos, herramientas o estructuras de distinto nivel")
        self.combo_riesgos.addItem("RC16 - Caída a piques")
        self.combo_riesgos.addItem("RC18 - Aplastamiento / Atrapamiento por caída de rocas en mina subterránea")
        self.combo_riesgos.addItem("RC19 - Estallido de roca")
        self.combo_riesgos.addItem("RC20 - Concentración ambiental peligrosa de polvo y sílice")
        self.combo_riesgos.addItem("RC22 - Deformación, inestabilidad y colapso de componentes en pasillos, pisos y barandas")
        self.combo_riesgos.addItem("RC23 - Colapso estructural en mina subterránea")
        self.combo_riesgos.addItem("RC24 - Desprendimiento y caída de talud en mina cielo abierto")
        self.combo_riesgos.addItem("RC25 - Choque / Colisión / Volcamiento de maquinarias")
        self.combo_riesgos.addItem("RC26 - Choque / Colisión / Volcamiento de equipos autónomos")
        self.combo_riesgos.addItem("RC27 - Atropello")
        self.combo_riesgos.addItem("RC28 - Airblast(Golpe de aire)")
        # Añade más opciones según los riesgos disponibles en tu documento
        
        self.combo_riesgos.currentIndexChanged.connect(self.mostrar_preguntas)
        layout_principal.addWidget(self.combo_riesgos)

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
                
        if index == 1:  # RC01 - Contacto con energía eléctrica
            preguntas = [
                {"codigo": "RC01-01", "pregunta": "¿Identifiqué el equipo y los puntos para el corte de energía (Aislación y bloqueo)?"},
                {"codigo": "RC01-02", "pregunta": "¿Instalé bloqueo con tarjeta(s) y candado(s) personal en el o los puntos y equipos correspondientes?"},
                {"codigo": "RC01-03", "pregunta": "¿Realicé y/o participé en las pruebas de verificación de ausencia de tensión y verifiqué la puesta a tierra antes de iniciar el trabajo?"},
                {"codigo": "RC01-04", "pregunta": "¿Verifiqué según check list que no existe fuga a tierra en las herramientas eléctricas antes de iniciar el trabajo?"},
                {"codigo": "RC01-05", "pregunta": "¿Identifiqué las protecciones a equipos de inversión y están operativas?"}
            ]
        elif index == 2:  # RC02 - Caída de distinto nivel
            preguntas = [
                {"codigo": "RC02-01", "pregunta": "¿Verifiqué que la plataforma fija temporal se encuentra autorizada por personal competente?"},
                {"codigo": "RC02-02", "pregunta": "¿Verifiqué que se cumple con el programa de mantenimiento e inspección de las plataformas móviles?"}
            ]
        elif index == 3:  # RC03 - Aplastamiento / Atrapamiento por carga suspendida
            preguntas = [
                {"codigo": "RC03-01", "pregunta": "¿Verifiqué que los elementos y los equipos de izaje son los indicados en el plan de izaje y que se encuentran en buen estado para la maniobra?"},
                {"codigo": "RC03-02", "pregunta": "¿Las condiciones climáticas y del entorno (estructuras, líneas eléctricas, etc.) permiten realizar las maniobras de izaje de manera segura?"}
            ]
        elif index == 4:  # RC04 - Proyección descontrolada de líquidos a alta presión
            preguntas = [
                {"codigo": "RC04-01", "pregunta": "¿Verifiqué los elementos para control y/o ausencia de presión de los sistemas neumáticos o hidráulicos que intervendré?"},
                {"codigo": "RC04-02", "pregunta": "¿Verifiqué que los dispositivos de contención de energía se encuentren operativos e instalados en terreno según estándar? (Ej.: Cadenas, piolas de seguridad, entre otros)"}
            ]
        elif index == 5:  # RC05 - Caída de roca a cielo abierto
            preguntas = [
                {"codigo": "RC05-01", "pregunta": "¿Realicé inspección visual, verifiqué y registré que las áreas a intervenir estén libres de riesgos eminentes o potenciales de caídas de rocas antes del ingreso a trabajar?"},
                {"codigo": "RC05-02", "pregunta": "¿Me dieron a conocer el mapa de riesgos geotécnicos actualizado y sus respectivas recomendaciones, para las zonas donde se trabajará?"}
            ]
        elif index == 6:  # RC06 - Incendio
            preguntas = [
                {"codigo": "RC06-01", "pregunta": "¿Mi área de trabajo se encuentra libre de ser afectada por un incendio de acuerdo al mapa de riesgos?"},
                {"codigo": "RC06-02", "pregunta": "¿Uso los EPP definidos para el trabajo y se encuentran en buenas condiciones? (Traje, pechera, polainas, guantes, careta facial)"}
            ]
        elif index == 7:  # RC07 - Contacto con sustancias químicas peligrosas
            preguntas = [
                {"codigo": "RC07-01", "pregunta": "¿Conozco los riesgos de la sustancia química a utilizar y los controles que debo aplicar?"},
                {"codigo": "RC07-02", "pregunta": "¿Estoy capacitado para el uso de los EPP específicos para la tarea?"}
            ]
        elif index == 8:  # RC08 - Atrapamiento / Aprisionamiento con partes móviles
            preguntas = [
                {"codigo": "RC08-01", "pregunta": "¿Verifiqué que existan guardas o protecciones en zonas donde hay piezas en movimiento o partes móviles y estas se encuentran en buen estado?"},
                {"codigo": "RC08-02", "pregunta": "¿Estoy en conocimiento de cómo activar los sistemas de parada de emergencias de mi área de trabajo?"}
            ]
        elif index == 9:  # RC9 - Choque / Colisión / Volcamiento de vehículo
            preguntas = [
                {"codigo": "RC9-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC9-02", "pregunta": "¿Me informé del estado de la ruta y sus restricciones? (velocidad, reparaciones y autorizaciones necesarias, establecidas en el Plan de tránsito)"}
            ]
        elif index == 10:  # RC10 - Exposición a atmósferas peligrosas en espacios confinados
            preguntas = [
                {"codigo": "RC10-01", "pregunta": "¿El espacio confinado que voy a intervenir está señalizado? ¿La señalética indica su clasificación y los gases/temperatura a monitorear?"},
                {"codigo": "RC10-02", "pregunta": "¿He sido capacitado en el correcto uso de la protección respiratoria seleccionada para intervenir este espacio confinado?"}
            ]
        elif index == 11:  # RC11| - Contacto con material fundido
            preguntas = [
                {"codigo": "RC11-01", "pregunta": "¿Uso los EPP definidos para el trabajo y se encuentran en buenas condiciones? (Traje, pechera, polainas, guantes, careta facial)"},
                {"codigo": "RC11-02", "pregunta": "¿Verifiqué que las condiciones de humedad del entorno y realicé chequeo de funcionamiento del sistema de bombeo?"}
            ]
        elif index == 12:  # RC12 - Caída de objetos, herramientas o estructuras de distinto nivel
            preguntas = [
                {"codigo": "RC12-01", "pregunta": "¿Verifiqué efectivamente que no existan trabajos en la vertical al momento de iniciar la tarea?"},
                {"codigo": "RC12-02", "pregunta": "¿Verifiqué que no existan objetos sobre o entre medio de estructuras de equipos que puedan caer a distinto nivel y golpear a una o varias personas?"}
            ]
        elif index == 13:  # RC13 - Caída a piques
            preguntas = [
                {"codigo": "RC13-01", "pregunta": "¿Uso los EPP definidos para el trabajo y se encuentran en buenas condiciones? (cola de seguridad y arnés de seguridad)"},
                {"codigo": "RC13-02", "pregunta": "¿Verifiqué que los puntos de vaciado cuentan con muros tope que impidan la caída, que no presenten daño y que se encuentren limpios?"}
            ]
        elif index == 14:  # RC14 - Aplastamiento / Atrapamiento por caída de rocas en mina subterránea
            preguntas = [
                {"codigo": "RC14-01", "pregunta": "¿Revisé la frente, galerías, fortificación (incluyendo materialidades tales como soportes de pilares y vigas de madera) y sectores con riesgo de caída de roca después de un proceso de tronadura?"},
                {"codigo": "RC14-02", "pregunta": "¿Antes de iniciar mis actividades me aseguro de que el equipo que voy a operar y/o jaulas de protección, se encuentra en buenas condiciones?"}
            ]
        elif index == 15:  # RC15 - Estallido de roca
            preguntas = [
                {"codigo": "RC15-01", "pregunta": "¿He recibido la información respecto a las zonas seguras para trabajar por parte de mi supervisor? (Zonas de transición, procesos de fortificación, información geo mecánica)."},
                {"codigo": "RC15-02", "pregunta": "¿Conozco los puntos de encuentro y rutas de evacuación?"}
            ]
        elif index == 16:  # RC16 - Concentración ambiental peligrosa de polvo y sílice
            preguntas = [
                {"codigo": "RC16-01", "pregunta": "¿Me informaron del Nivel de riesgo por exposición a sílice del área a intervenir?"},
                {"codigo": "RC16-02", "pregunta": "¿Mi respirador es el adecuado (tipo, talla, filtro)? ¿Está en buenas condiciones y sé cómo usarlo?"}
            ]
        elif index == 17:  # RC17 - Deformación, inestabilidad y colapso de componentes en pasillos, pisos y barandas
            preguntas = [
                {"codigo": "RC17-01", "pregunta": "¿Verifiqué que el estado de estructuras como; sujeciones, barandas, escalas, grating, es el adecuado para el tránsito y desarrollo de actividades?"},
                {"codigo": "RC17-02", "pregunta": "¿Verifiqué que las áreas con estructuras dañadas o con falta de algún componente, se encuentren cerradas (barreras duras) y señalizadas correctamente?"}
            ]
        elif index == 18:  # RC18 - Colapso estructural en mina subterránea
            preguntas = [
                {"codigo": "RC18-01", "pregunta": "¿Al revisar mi entorno de trabajo me aseguro de chequear que la zona se encuentre estable, manteniendo atención a los signos de cambios de la roca?"},
                {"codigo": "RC18-02", "pregunta": "¿Verifiqué que la fortificación se encuentra en condiciones óptimas para realizar las tareas?"}
            ]
        elif index == 19:  # RC19 - Desprendimiento y caída de talud en mina cielo abierto
            preguntas = [
                {"codigo": "RC19-01", "pregunta": "¿En caso de personal que realiza saneamiento: Realicé inspección visual, verifiqué y corroboré que los registros de las áreas a intervenir estén libres de riesgos inminentes de caídas de rocas antes del ingreso a trabajar?"},
                {"codigo": "RC19-02", "pregunta": "En caso de ser operador de equipo: ¿me aseguré de que el área se saneó y estabilizó antes de realizar mis labores?"}
            ]
        elif index == 20:  # RC20 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC20-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC20-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 21:  # RC21 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC21-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC21-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 22:  # RC22 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC22-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC22-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 23:  # RC23 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC23-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC23-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 24:  # RC24 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC24-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC24-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 25:  # RC25 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC25-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC25-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 26:  # RC26 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC26-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC26-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 27:  # RC27 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC27-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC27-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        elif index == 28:  # RC28 - Choque / Colisión / Volcamiento de maquinarias
            preguntas = [
                {"codigo": "RC28-01", "pregunta": "¿Realicé la autoevaluación de condiciones físicas y psicológicas antes de conducir?"},
                {"codigo": "RC28-02", "pregunta": "¿Apliqué la lista de chequeo de la maquinaria industrial autopropulsada antes de operar?"}
            ]
        self.crear_seccion_preguntas(preguntas)

    def crear_seccion_preguntas(self, preguntas):
        self.variables_trabajador = []
        for pregunta in preguntas:
            etiqueta = QLabel(f"Cód: {pregunta['codigo']} - {pregunta['pregunta']}")
            etiqueta.setStyleSheet("font: 12pt 'Arial';")

            grupo_botones = QGroupBox()
            layout_botones = QHBoxLayout()
            grupo_botones.setLayout(layout_botones)

            variable = QButtonGroup()
            self.variables_trabajador.append((pregunta["codigo"], variable))

            boton_si = QRadioButton("Sí")
            boton_no = QRadioButton("No")
            layout_botones.addWidget(boton_si)
            layout_botones.addWidget(boton_no)

            variable.addButton(boton_si)
            variable.addButton(boton_no)

            self.layout_formulario.addRow(etiqueta, grupo_botones)

    def comprobar_respuestas(self):
        respuestas = [(codigo, grupo.checkedButton().text()) if grupo.checkedButton() else (codigo, None) for codigo, grupo in self.variables_trabajador]
        if any(respuesta is None for _, respuesta in respuestas):
            QMessageBox.warning(self, "Error", "Por favor responda todas las preguntas antes de continuar.")
            return
        
        for codigo, respuesta in respuestas:
            print(f"Código: {codigo}, Respuesta: {respuesta}")
            paso = 2
            tipo_respuesta = 'trabajador' 
            self.db.insertar_respuesta(self.id_art, tipo_respuesta, paso, codigo, respuesta)

        QMessageBox.information(self, "Éxito", "Datos guardados exitosamente.")
        self.abrir_formulario_trabajador_paso3(self.id_art)

    def abrir_formulario_trabajador_paso3(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_trabajador_paso3(id_art)
        self.app = ventana
        self.app.show()