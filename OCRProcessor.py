import easyocr
import time
import re
import cv2  # Importar OpenCV para mostrar la imagen
import numpy as np  # Para manipulación de imágenes con OpenCV
import os

class OCRProcessor:
    def __init__(self, language='es', use_gpu=False):
        # Inicializar el lector de EasyOCR
        self.reader = easyocr.Reader([language], gpu=use_gpu)
        self.transcurred_time = 0
    
    @staticmethod
    def clean_text(text):
        """
        Limpia el texto, preservando caracteres españoles.
        - Reemplaza 'ü' por 'ú'.
        - Elimina caracteres no alfabéticos o no numéricos, excepto espacios.
        """
        text = text.replace('ü', 'ú')  # Reemplazar 'ü' por 'ú'
        text = re.sub(r'[^A-Za-zÁÉÍÓÚáéíóúÑñÜü0-9\s]', '', text)  # Mantener caracteres válidos
        return text.strip()
    
    @staticmethod
    def is_number(text):
        """
        Verifica si el texto es un número válido (con punto o coma decimal).
        """
        return bool(re.match(r'^\d+[\.\,]?\d*$', text))
 
    @staticmethod
    def get_area(coords):
        """
        Calcular el área de la caja delimitadora (bounding box) a partir de las coordenadas.
        """
        # Calcular el área de la caja delimitadora: (ancho * alto)
        width = coords[1][0] - coords[0][0]
        height = coords[2][1] - coords[0][1]
        return width * height
 
    @staticmethod
    def combine_lines(results, threshold=20):
        """
        Combina las líneas de texto cercanas, siempre y cuando no sean precios.
        Si el texto es un número (precio), no se combina.

        Args:
            results (list): Lista de resultados del OCR, cada uno con texto y coordenadas.
            threshold (int): Distancia máxima entre el final de un texto y el inicio de otro para combinarlos.

        Returns:
            list: Lista de tuplas con el texto combinado y las coordenadas ajustadas.
        """
        combined_results = []  # Lista para almacenar los resultados combinados
        current_text = ""  # Texto combinado
        current_coords = None  # Coordenadas combinadas del texto
        current_right = 0  # Coordenada X del extremo derecho del texto actual

        for item in results:
            # Verificar si el formato es el esperado
            if len(item) >= 2:
                coords = item[0]
                text = item[1]
            else:
                continue  # Si no se cumple el formato, saltar el elemento

            clean_line = OCRProcessor.clean_text(text)

            # Si el texto es un número, se guarda como un precio por separado
            if OCRProcessor.is_number(clean_line):
                # Si hay texto acumulado, lo guardamos primero
                if current_text:
                    combined_results.append((current_text, current_coords))
                    current_text = ""  # Reiniciar texto acumulado
                    current_coords = None  # Reiniciar coordenadas acumuladas

                # Guardar el precio actual
                combined_results.append((clean_line, coords))
                continue  # Pasar al siguiente texto

            # Si no es un número, procedemos a combinarlo con el texto anterior si está cerca
            if current_text:
                # Obtener las coordenadas de la esquina derecha del texto actual
                current_right = current_coords[1][0]

                # Obtener la coordenada de la esquina izquierda del nuevo texto
                new_left = coords[0][0]

                # Si el texto está suficientemente cerca, los combinamos
                if abs(new_left - current_right) < threshold:
                    current_text += " " + clean_line  # Combinar con espacio
                    # Actualizar las coordenadas combinadas (mantener las más alejadas)
                    current_coords = [
                        current_coords[0],  # Esquina superior izquierda del primero
                        (max(current_coords[1][0], coords[1][0]), current_coords[1][1]),  # Esquina superior derecha
                        coords[2],  # Esquina inferior derecha del nuevo
                        (current_coords[3][0], max(current_coords[3][1], coords[3][1]))  # Esquina inferior izquierda
                    ]
                else:
                    # Si no están cerca, guardamos el texto actual y comenzamos uno nuevo
                    combined_results.append((current_text, current_coords))
                    current_text = clean_line  # Iniciar con el nuevo texto
                    current_coords = coords  # Coordenadas del nuevo texto

            else:
                # Si no hay texto acumulado, solo asignamos el texto y las coordenadas
                current_text = clean_line
                current_coords = coords

        # Añadir el último texto si existe
        if current_text:
            combined_results.append((current_text, current_coords))

        return combined_results

    def process_image(self, image_path, show_img=False):
        """
        Procesa una imagen para extraer nombres y precios utilizando EasyOCR.
        
        Args:
            image_path (str): Ruta de la imagen a procesar.
        
        Returns:
            list[dict]: Lista de diccionarios con 'name' y 'price'.
        """
        # Leer la imagen con OCR
        start_time = time.time()
        results = self.reader.readtext(image_path)
        
        if not results:
            print("No se encontraron textos en la imagen.")
            return []
        
        # Combinar líneas cercanas
        combined_results = self.combine_lines(results)
        #print(combined_results)
        
        # Lista para almacenar los resultados
        extracted_data = []

        # Procesar resultados combinados
        i = 0
        while i < len(combined_results):
            text_name = self.clean_text(combined_results[i][0])
            if i + 1 < len(combined_results):
                next_text = self.clean_text(combined_results[i + 1][0])
                if self.is_number(next_text):
                    extracted_data.append({'name': text_name, 'price': next_text})
                    i += 2  # Saltar al siguiente par
                else:
                    extracted_data.append({'name': text_name, 'price': None})
                    i += 1  # Avanzar uno si el siguiente no es un precio
            else:
                extracted_data.append({'name': text_name, 'price': None})
                i += 1

        # Filtrar solo los elementos que tienen precio
        filtered_data = [item for item in extracted_data if item['price'] is not None]
        
        # Mostrar la imagen con las áreas y el texto
        if show_img:
            self.show_image_with_text(image_path, results)
        
        end_time = time.time()
        self.transcurred_time = end_time - start_time
        return filtered_data

    def show_image_with_text(self, image_path, results):
        """
        Muestra la imagen con las áreas de texto detectadas y el texto correspondiente.
        
        Args:
            image_path (str): Ruta de la imagen a mostrar.
            results (list): Resultados de OCR con coordenadas y texto.
        """
        # Leer la imagen usando OpenCV
        image = cv2.imread(image_path)

        for item in results:
            # Obtener las coordenadas y el texto
            coords = item[0]
            text = item[1]

            # Dibujar el rectángulo alrededor del texto detectado
            pts = np.array(coords, dtype=np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(image, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Poner el texto sobre la imagen
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (int(coords[0][0]), int(coords[0][1] - 10)), font, 0.5, (0, 255, 0), 2)

        # Guardar la imagen con texto
        output_path = "output_image_with_text.jpg"
        cv2.imwrite(output_path, image)

        # Abrir la imagen guardada automáticamente con el visor predeterminado del sistema
        os.startfile(output_path)