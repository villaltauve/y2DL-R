from pytubefix import YouTube
from moviepy import AudioFileClip
import os
import subprocess
import re

class DescargadorYouTube:
    def __init__(self, url, carpeta, resolucion, convertir_mp3, progreso_callback=None):
        self.url = url
        self.carpeta = carpeta
        self.resolucion = resolucion
        self.convertir_mp3 = convertir_mp3
        self.progreso_callback = progreso_callback

    def descargar(self):
        try:
            print(f"Descargando: '{self.url}'")  # Depuración: muestra la URL exacta
            yt = YouTube(self.url, on_progress_callback=self.progreso_callback)
            resolucion_num = int(self.resolucion[:-1])  # Ejemplo: "1080p" -> 1080
            # Limpiar el título para usarlo como nombre de archivo seguro
            safe_title = re.sub(r'[^\w\-_. ]', '_', yt.title)

            if resolucion_num > 720:
                # Para resoluciones altas, descargar video y audio por separado
                video_stream = yt.streams.filter(progressive=False, file_extension='mp4', resolution=self.resolucion).first()
                audio_stream = yt.streams.filter(only_audio=True).first()

                if not video_stream or not audio_stream:
                    raise Exception(f"No se encontró la resolución {self.resolucion} o el audio para este video.")

                # Descargar video y audio
                video_path = video_stream.download(output_path=self.carpeta, filename="temp_video.mp4")
                audio_path = audio_stream.download(output_path=self.carpeta, filename="temp_audio.mp4")

                # Unir video y audio con ffmpeg
                output_path = os.path.join(self.carpeta, f"{safe_title}.mp4")
                subprocess.run([
                    "ffmpeg", "-i", video_path, "-i", audio_path,
                    "-c:v", "copy", "-c:a", "aac", output_path
                ], check=True)

                # Limpiar archivos temporales
                os.remove(video_path)
                os.remove(audio_path)

                if self.convertir_mp3:
                    ruta_mp3 = output_path.replace(".mp4", ".mp3")
                    clip = AudioFileClip(output_path)
                    clip.write_audiofile(ruta_mp3)
                    clip.close()
                    os.remove(output_path)

            else:
                # Para resoluciones bajas, usar stream progresivo
                stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
                video = next((s for s in stream if s.resolution == self.resolucion), stream.first())

                if not video:
                    raise Exception(f"No se encontró la resolución {self.resolucion} para este video.")

                archivo_salida = video.download(output_path=self.carpeta, filename=f"{safe_title}.mp4")

                if self.convertir_mp3:
                    ruta_mp3 = archivo_salida.replace(".mp4", ".mp3")
                    clip = AudioFileClip(archivo_salida)
                    clip.write_audiofile(ruta_mp3)
                    clip.close()
                    os.remove(archivo_salida)

            return True

        except Exception as e:
            raise Exception(f"Error al descargar el video: {str(e)}")
