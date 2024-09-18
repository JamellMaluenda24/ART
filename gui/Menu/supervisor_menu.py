from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QMessageBox, QTableWidget, QTableWidgetItem, QInputDialog, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Controladores.Controlador_Pasos import ControladorPasos
from Controladores.Controlador_Sesion_BD import ControladorBaseDatos
from Controladores.Controlador_ART_BD import ControladorARTconBD 
from Controladores.FormularioART.CreacionART import PDFRellenador
from datetime import datetime, timedelta

class SupervisorMenuApp(QMainWindow):
    def __init__(self, rut):
        super().__init__()
        self.setWindowTitle("WWS- Supervisor")
        self.setStyleSheet("background-color: #ecf0f1;")
        self.controlador_bd = ControladorBaseDatos()
        self.controlador_ART_BD = ControladorARTconBD()
        self.rut = rut

        # Layout principal
        layout_principal = QHBoxLayout()

        # Frame de la barra lateral
        self.frame_lateral = QFrame()
        self.frame_lateral.setStyleSheet("background-color: #2c3e50;")
        layout_lateral = QVBoxLayout()
        self.frame_lateral.setLayout(layout_lateral)

        # Frame del contenido principal
        self.frame_contenido_principal = QFrame()
        layout_contenido_principal = QVBoxLayout()
        self.frame_contenido_principal.setLayout(layout_contenido_principal)

        # Añadir la barra lateral y el contenido principal al layout principal
        layout_principal.addWidget(self.frame_lateral, 1)
        layout_principal.addWidget(self.frame_contenido_principal, 4)

        # Configurar la ventana principal
        contenedor_principal = QWidget()
        contenedor_principal.setLayout(layout_principal)
        self.setCentralWidget(contenedor_principal)

        # Crear elementos de la barra lateral
        self.crear_barra_lateral(layout_lateral)

        # Crear contenido principal inicial
        self.crear_contenido_principal(layout_contenido_principal)
        self.showMaximized()  # Mostrar la ventana maximizada

        # Ajustar geometría después de mostrar
        self.adjust_geometria()

    def crear_barra_lateral(self, layout):
        etiqueta_titulo = QLabel("WSS Supervisor")
        etiqueta_titulo.setAlignment(Qt.AlignCenter)
        etiqueta_titulo.setFont(QFont("Arial", 18, QFont.Bold))
        etiqueta_titulo.setStyleSheet("color: white; padding: 20px;")
        layout.addWidget(etiqueta_titulo)
        
        boton_informes = QPushButton("Informes")
        boton_informes.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_informes.clicked.connect(self.mostrar_informes)
        layout.addWidget(boton_informes)

        boton_completar_art = QPushButton("Completar ART")
        boton_completar_art.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_completar_art.clicked.connect(self.pedir_id_art)
        layout.addWidget(boton_completar_art)

        boton_configuracion = QPushButton("Configuración")
        boton_configuracion.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_configuracion.clicked.connect(self.mostrar_configuracion)
        layout.addWidget(boton_configuracion)

        boton_art_responder = QPushButton("ART a Responder")
        boton_art_responder.setStyleSheet("padding: 15px; background-color: #3498db; color: white; border: none; border-radius: 5px;")
        boton_art_responder.clicked.connect(self.mostrar_art_a_responder)
        layout.addWidget(boton_art_responder)

        # Nuevo botón para generar ART
        boton_generar_art = QPushButton("Generar ART")
        boton_generar_art.setStyleSheet("padding: 15px; background-color: #2ecc71; color: white; border: none; border-radius: 5px;")
        boton_generar_art.clicked.connect(self.generar_art)
        layout.addWidget(boton_generar_art)

        layout.addStretch()

    def crear_contenido_principal(self, layout):
        etiqueta_bienvenida = QLabel("Bienvenido al menú del Supervisor")
        etiqueta_bienvenida.setAlignment(Qt.AlignCenter)
        etiqueta_bienvenida.setStyleSheet("font: bold 24pt; color: #2c3e50; margin-top: 50px;")
        layout.addWidget(etiqueta_bienvenida)

    def mostrar_informes(self):
        self.limpiar_contenido_principal()

        etiqueta_informes = QLabel("Informes")
        etiqueta_informes.setAlignment(Qt.AlignCenter)
        etiqueta_informes.setStyleSheet("font: bold 20pt; color: #2c3e50; margin-top: 20px;")
        self.frame_contenido_principal.layout().addWidget(etiqueta_informes)

    def mostrar_configuracion(self):
        self.limpiar_contenido_principal()
        
        etiqueta_configuracion = QLabel("Configuración")
        etiqueta_configuracion.setAlignment(Qt.AlignCenter)
        etiqueta_configuracion.setStyleSheet("font: bold 20pt; color: #2c3e50; margin-top: 20px;")
        self.frame_contenido_principal.layout().addWidget(etiqueta_configuracion)

    def mostrar_art_a_responder(self):
        print("Mostrando ART a Responder")  # Agregado para depuración
        self.limpiar_contenido_principal()

        titulo_art_responder = QLabel("ART a Responder")
        titulo_art_responder.setAlignment(Qt.AlignCenter)
        titulo_art_responder.setFont(QFont("Arial", 20, QFont.Bold))
        titulo_art_responder.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        self.frame_contenido_principal.layout().addWidget(titulo_art_responder)

        layout_tablas = QVBoxLayout()

        # Tabla de ART en espera
        self.tabla_art_en_espera = QTableWidget()
        self.tabla_art_en_espera.setColumnCount(10)
        self.tabla_art_en_espera.setHorizontalHeaderLabels([
            "ID ART", "RUT Trabajador", "Empresa", "Gerencia", "Fecha", "Hora Inicio",
            "Hora Término", "Superintendencia", "Trabajo a Realizar", "Estado"
        ])
        self.tabla_art_en_espera.setStyleSheet("font: 12pt; color: #34495e;")
        layout_tablas.addWidget(QLabel("ART en Espera"))
        layout_tablas.addWidget(self.tabla_art_en_espera)

        # Tabla de ART aprobadas
        self.tabla_art_aprobadas = QTableWidget()
        self.tabla_art_aprobadas.setColumnCount(10)
        self.tabla_art_aprobadas.setHorizontalHeaderLabels([
            "ID ART", "RUT Trabajador", "Empresa", "Gerencia", "Fecha", "Hora Inicio",
            "Hora Término", "Superintendencia", "Trabajo a Realizar", "Estado"
        ])
        self.tabla_art_aprobadas.setStyleSheet("font: 12pt; color: #34495e;")
        layout_tablas.addWidget(QLabel("ART Aprobadas"))
        layout_tablas.addWidget(self.tabla_art_aprobadas)

        self.frame_contenido_principal.layout().addLayout(layout_tablas)
        self.cargar_art_a_responder()

    def cargar_art_a_responder(self):
        art_a_responder = self.controlador_ART_BD.obtener_art_a_responder()
        art_realizadas = self.controlador_ART_BD.obtener_art_realizadas_supervisor()  # Obtener todas las ART realizadas

        print("ART en Espera:", art_a_responder)  # Verifica los ART en espera
        print("ART Realizadas:", art_realizadas)  # Verifica todos los ART realizadas

        self.tabla_art_en_espera.setRowCount(0)
        self.tabla_art_aprobadas.setRowCount(0)

        for art in art_a_responder:
            fila = self.tabla_art_en_espera.rowCount()
            self.tabla_art_en_espera.insertRow(fila)
            self.tabla_art_en_espera.setItem(fila, 0, QTableWidgetItem(str(art["id_art"])))
            self.tabla_art_en_espera.setItem(fila, 1, QTableWidgetItem(art["trabajador_rut"]))
            self.tabla_art_en_espera.setItem(fila, 2, QTableWidgetItem(art["empresa"]))
            self.tabla_art_en_espera.setItem(fila, 3, QTableWidgetItem(art["gerencia"]))
            self.tabla_art_en_espera.setItem(fila, 4, QTableWidgetItem(str(art["fecha"])))
            self.tabla_art_en_espera.setItem(fila, 5, QTableWidgetItem(str(art["hora_inicio"])))
            self.tabla_art_en_espera.setItem(fila, 6, QTableWidgetItem(str(art["hora_termino"])))
            self.tabla_art_en_espera.setItem(fila, 7, QTableWidgetItem(art["superintendencia"]))
            self.tabla_art_en_espera.setItem(fila, 8, QTableWidgetItem(art["trabajo_realizar"]))
            self.tabla_art_en_espera.setItem(fila, 9, QTableWidgetItem(art["estado"]))

        for art in art_realizadas:
            if art["estado"] == "Aprobada":
                fila = self.tabla_art_aprobadas.rowCount()
                self.tabla_art_aprobadas.insertRow(fila)
                self.tabla_art_aprobadas.setItem(fila, 0, QTableWidgetItem(str(art["id_art"])))
                self.tabla_art_aprobadas.setItem(fila, 1, QTableWidgetItem(art["trabajador_rut"]))
                self.tabla_art_aprobadas.setItem(fila, 2, QTableWidgetItem(art["empresa"]))
                self.tabla_art_aprobadas.setItem(fila, 3, QTableWidgetItem(art["gerencia"]))
                self.tabla_art_aprobadas.setItem(fila, 4, QTableWidgetItem(str(art["fecha"])))
                self.tabla_art_aprobadas.setItem(fila, 5, QTableWidgetItem(str(art["hora_inicio"])))
                self.tabla_art_aprobadas.setItem(fila, 6, QTableWidgetItem(str(art["hora_termino"])))
                self.tabla_art_aprobadas.setItem(fila, 7, QTableWidgetItem(art["superintendencia"]))
                self.tabla_art_aprobadas.setItem(fila, 8, QTableWidgetItem(art["trabajo_realizar"]))
                self.tabla_art_aprobadas.setItem(fila, 9, QTableWidgetItem(art["estado"]))

        print("Número de filas en ART en Espera:", self.tabla_art_en_espera.rowCount())
        print("Número de filas en ART Aprobadas:", self.tabla_art_aprobadas.rowCount())

        self.tabla_art_en_espera.resizeColumnsToContents()
        self.tabla_art_aprobadas.resizeColumnsToContents()

    def limpiar_contenido_principal(self):
        for i in reversed(range(self.frame_contenido_principal.layout().count())):
            widget = self.frame_contenido_principal.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

    def pedir_id_art(self):
        id_art, ok = QInputDialog.getText(self, "Completar ART", "Ingrese la ID de ART:")
        if ok and id_art:
            self.abrir_formulario_paso1(id_art)

    def generar_art(self):
        # Obtener las ART aprobadas para generar
        art_aprobadas = []

        # Recorre la tabla de ART aprobadas para identificar cuáles están en estado "Aprobada"
        for fila in range(self.tabla_art_aprobadas.rowCount()):
            id_art = self.tabla_art_aprobadas.item(fila, 0).text()  # ID de ART
            estado = self.tabla_art_aprobadas.item(fila, 9).text()  # Estado de ART
            
            if estado.lower() == "aprobada":
                art_aprobadas.append(id_art)
        
        if not art_aprobadas:
            QMessageBox.information(self, "Generar ART", "No hay ART aprobadas para generar.")
            return

        # Solicitar al usuario seleccionar una ART aprobada
        id_art, ok = QInputDialog.getItem(self, "Generar ART", "Seleccione la ID de la ART aprobada para generar:", art_aprobadas, 0, False)
        
        if ok and id_art:
            # Generar el PDF utilizando la clase PDFRellenador
            try:
                pdf_path = r"C:\Users\ALUMNO\Desktop\Jamell\Art Interfaz Oficial\Controladores\FormularioART\PlantillaART\PlantillaART.pdf"  # Ruta completa al template de PDF base

                # Mostrar el diálogo para seleccionar la ubicación donde se guardará el archivo
                opciones = QFileDialog.Options()
                opciones |= QFileDialog.DontUseNativeDialog
                archivo_seleccionado, _ = QFileDialog.getSaveFileName(self, "Guardar ART generada", f"ART_{id_art}_generada.pdf", "PDF Files (*.pdf)", options=opciones)
                
                # Verificar si el usuario seleccionó una ubicación
                if archivo_seleccionado:
                    # Crear la instancia de PDFRellenador con el id_art
                    rellenador = PDFRellenador(pdf_path, id_art)

                    # Rellenar y generar el PDF en la ubicación seleccionada por el usuario
                    rellenador.rellenar_pdf(archivo_seleccionado)

                    QMessageBox.information(self, "Generar ART", f"ART con ID {id_art} generada exitosamente en {archivo_seleccionado}.")
                else:
                    QMessageBox.information(self, "Generar ART", "No se seleccionó ninguna ubicación para guardar el archivo.")
                    
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al generar la ART: {str(e)}")
                print(f"Detalles del error: {e}")  # Imprimir detalles en la consola



    def adjust_geometria(self):
        # Ajustar la geometría después de mostrar la ventana
        self.resize(self.sizeHint())  # Ajustar el tamaño basado en las sugerencias
        self.showMaximized()  # Mostrar maximizada nuevamente

    def abrir_formulario_paso1(self, id_art):
        self.close()
        ventana = ControladorPasos.abrir_formulario_supervisor_paso1(id_art)
        self.app = ventana
        self.app.show()
