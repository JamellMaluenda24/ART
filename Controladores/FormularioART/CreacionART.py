import os
import fitz  # PyMuPDF
from mysql.connector import Error
from database.db_connection import MySQLConnection

class PDFRellenador:
    def __init__(self, pdf_path, art_id):
        """
        Constructor para inicializar el PDF y la conexión MySQL.
        :param pdf_path: Ruta del archivo PDF que se va a rellenar.
        :param art_id: Identificador del ART cuyas respuestas se van a rellenar.
        """
        self.pdf_path = pdf_path
        self.art_id = art_id
        self.pdf_documento = None
        self.conexion = MySQLConnection()

    def abrir_pdf(self):
        """
        Abre el archivo PDF.
        """
        self.pdf_documento = fitz.open(self.pdf_path)

    def obtener_respuestas(self):
        """
        Obtiene las respuestas de la base de datos para el ART.
        :return: Lista de respuestas.
        """
        query = """
        SELECT numero_pregunta, respuesta_texto, respuesta_seleccion 
        FROM respuesta_art 
        WHERE art_id = %s
        """
        self.conexion.connect()
        try:
            respuestas = self.conexion.execute_query(query, params=(self.art_id,), fetch_all=True)
            return respuestas
        except Error as e:
            print(f"Error al obtener respuestas: {e}")
            return []
        finally:
            self.conexion.close()

    def insertar_respuestas_en_pdf(self, respuestas):
        """
        Inserta las respuestas en el PDF en las posiciones correspondientes.
        :param respuestas: Lista de respuestas extraídas de la base de datos.
        """
        num_paginas = len(self.pdf_documento)  # Obtener el número total de páginas

        for respuesta in respuestas:
            numero_pregunta, respuesta_texto, respuesta_seleccion = respuesta

            # Generar el texto de respuesta
            if respuesta_seleccion == 'si':
                texto_respuesta = "Sí"
            elif respuesta_seleccion == 'no':
                texto_respuesta = "No"
            else:
                texto_respuesta = respuesta_texto

            # Aquí asumimos que cada pregunta se coloca en una página específica
            # Asegúrate de que no intentas acceder a una página que no existe
            for pagina_num in range(num_paginas):
                pagina = self.pdf_documento[pagina_num]
                # Ajusta las coordenadas X y Y según sea necesario
                pagina.insert_text((100, 100 + (pagina_num * 20)), f"{numero_pregunta}: {texto_respuesta}")

    def guardar_pdf(self, output_pdf_path):
        """
        Guarda el PDF con las respuestas añadidas.
        :param output_pdf_path: Ruta del archivo PDF donde se guardará el resultado.
        """
        self.pdf_documento.save(output_pdf_path)

    def cerrar_pdf(self):
        """
        Cierra el archivo PDF.
        """
        if self.pdf_documento:
            self.pdf_documento.close()

    def rellenar_pdf(self, output_pdf_name):
        """
        Función principal que ejecuta todos los pasos: abre el PDF, obtiene las respuestas y las inserta en el PDF.
        :param output_pdf_name: Nombre del archivo PDF donde se guardará el resultado.
        """
        # Obtener la ruta del escritorio
        escritorio_path = os.path.expanduser("~/Desktop")
        # Crear la ruta completa para el archivo PDF
        output_pdf_path = os.path.join(escritorio_path, output_pdf_name)
        
        self.abrir_pdf()
        respuestas = self.obtener_respuestas()
        if respuestas:
            self.insertar_respuestas_en_pdf(respuestas)
            self.guardar_pdf(output_pdf_path)
        self.cerrar_pdf()
        print(f"PDF rellenado guardado en {output_pdf_path}")

# Ejemplo de uso
pdf_path = r"C:\Users\ALUMNO\Desktop\Jamell\Art Interfaz Oficial\Controladores\FormularioART\PlantillaART\PlantillaART.pdf"
art_id = 123  # Ejemplo de ID de ART
output_pdf_name = f"ART_{art_id}_generada.pdf"  # Nombre del archivo PDF generado

rellenador = PDFRellenador(pdf_path, art_id)
rellenador.rellenar_pdf(output_pdf_name)
