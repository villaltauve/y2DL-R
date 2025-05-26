# YouTube Downloader - Instrucciones de uso

## Requisitos
- Python 3.8 o superior
- ffmpeg instalado y en el PATH

## Instalación
1. Instala Python desde https://www.python.org/downloads/
2. Instala las dependencias. Abre una terminal en la carpeta del proyecto y ejecuta:
   pip install -r requirements.txt
3. Descarga ffmpeg desde https://ffmpeg.org/download.html
   - Extrae el zip y agrega la carpeta `bin` de ffmpeg a la variable de entorno PATH de Windows.
   - Verifica que funcione ejecutando en la terminal:
     ffmpeg -version

## Uso
1. Ejecuta la aplicación con:
   python main.py
2. Pega la URL de YouTube, elige la carpeta de destino, la resolución y si quieres convertir a MP3.
3. Haz clic en "Descargar".

## Notas
- Si tienes problemas con la descarga o la conversión, asegúrate de que ffmpeg esté correctamente instalado y en el PATH.
- Los videos con caracteres especiales en el título se guardarán con un nombre seguro automáticamente. 