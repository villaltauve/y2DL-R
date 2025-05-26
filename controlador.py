from tkinter import filedialog, messagebox
from modelo import DescargadorYouTube
from pytubefix import YouTube

class Controlador:
    def __init__(self):
        self.vista = None

    def set_vista(self, vista):
        self.vista = vista

    def elegir_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.vista.set_carpeta(carpeta)

    def on_progreso(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        porcentaje = int((bytes_downloaded / total_size) * 100)
        self.vista.actualizar_barra(porcentaje)

    def iniciar_descarga(self):
        datos = self.vista.obtener_datos()

        # Validar URL
        if not datos["url"]:
            messagebox.showerror("Error", "Por favor, ingresa una URL válida.")
            return

        # Validar carpeta
        if not datos["carpeta"]:
            messagebox.showerror("Error", "Por favor, selecciona una carpeta de destino.")
            return

        try:
            self.vista.mostrar_mensaje("Descargando...")
            self.vista.actualizar_barra(0)
            self.vista.deshabilitar_boton()

            descargador = DescargadorYouTube(
                url=datos["url"],
                carpeta=datos["carpeta"],
                resolucion=datos["resolucion"],
                convertir_mp3=datos["convertir_mp3"],
                progreso_callback=self.on_progreso
            )

            descargador.descargar()
            self.vista.mostrar_mensaje("¡Descarga completada!")
            self.vista.actualizar_barra(100)
            messagebox.showinfo("Éxito", "Video descargado correctamente.")

        except Exception as e:
            self.vista.mostrar_mensaje("Error.")
            self.vista.actualizar_barra(0)
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

        finally:
            self.vista.habilitar_boton()
