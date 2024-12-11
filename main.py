print("Inicializando el modelo OCR...")
import os
import json
from tqdm import tqdm

from OCRProcessor import OCRProcessor

def print_data(extracted_data):
    # Mostrar los resultados
    print("\n--- Datos Extraídos con Precio ---")
    for item in extracted_data:
        print(f"Nombre: {item['name']}, Precio: {item['price']}")

def save_results_as_json(image_path, results): 
    # Crear el nombre del archivo JSON 
    base_name = os.path.basename(image_path) 
    name, _ = os.path.splitext(base_name) 
    json_path = os.path.join(os.path.dirname(image_path), f"{name}.json") 
    # Guardar los resultados en un archivo JSON 
    with open(json_path, 'w', encoding='utf-8') as json_file: 
        json.dump(results, json_file, ensure_ascii=False, indent=4)

def process_all_images_in_folder(ocr_processor, folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    with tqdm(total=len(image_files), desc="Procesando imágenes", unit="imagen", leave=True) as pbar:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            extracted_data = ocr_processor.process_image(image_path)
            save_results_as_json(image_path, extracted_data)
            print_data(extracted_data)
            pbar.update(1)

# Ejemplo de uso
if __name__ == "__main__":
    folder_path = 'images' 
    print("Inicializando modelo AI...")
    ocr_processor = OCRProcessor(language='es', use_gpu=False)
    process_all_images_in_folder(ocr_processor, folder_path)
    
    # Crear una instancia de OCRProcessor
    # ocr_processor = OCRProcessor(language='es', use_gpu=False)
    
    #Procesar una imagen
    # image_path = 'bbbb.jpg'
    # extracted_data = ocr_processor.process_image(image_path)
    
    # print(ocr_processor.transcurred_time)
    # print_data(extracted_data)
    # save_results_as_json(image_path, extracted_data)
    
    # print_data(ocr_processor.process_image('aaaa.jpg', True))
    # print(ocr_processor.transcurred_time)
    # save_results_as_json('aaaa.jpg', extracted_data)
