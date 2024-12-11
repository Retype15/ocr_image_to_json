# Proyecto de OCR con EasyOCR

## Descripción
Este proyecto utiliza EasyOCR para procesar imágenes y extraer texto, en este momento nombres de platos y sus precios de imagenes de menus, pero se puede modificar y adaptar a sus necesidades. Los resultados se guardan en archivos JSON correspondientes a cada imagen procesada. El procesamiento se realiza de manera eficiente utilizando operaciones de preprocesamiento de imágenes con OpenCV.

## Requisitos
- Python 3.12.3+
- easyocr
- opencv-python
- numpy
- tqdm

Puedes instalar las dependencias utilizando pip:

```bash
pip install easyocr opencv-python numpy tqdm
```

## Estructura del Proyecto
- `main.py`: Script principal que ejecuta el procesamiento de imágenes y guarda los resultados en JSON.
- `OCRProcessor.py`: Clase que contiene los métodos para procesar imágenes y extraer texto.
- `win_execute.sh`: Script de shell para ejecutar `main.py` en Linux/macOS.
- `linux_execute.bat`: Archivo por lotes para ejecutar `main.py` en Windows.
- `linux_setup.sh`: Script de configuración para otorgar permisos de ejecución y ejecutar `linux_execute.sh`.

## Uso
### Linux/macOS
1. Dar permisos de ejecución con 
```sh
chmod +x setup.sh./setup.sh
```
o ejecutar `linux_setup.sh`:

2. Después de la configuración, puedes ejecutar directamente `linux_execute.sh`.


### Windows
1. Ejecutar `win_execute.bat`:
   - Haz doble clic en `win_execute.bat`.

### Procesar Todas las Imágenes en una Carpeta
El script `main.py` está configurado para procesar todas las imágenes en la carpeta `images` y guardar los resultados en archivos JSON correspondientes.


## Ejemplo de Uso:
```
python main.py
```


## Autor
Desarrollado por Rety.

## Licencia
Este proyecto no tiene licencia, por lo que es libre de usarlo y cambiarlo a placer.
