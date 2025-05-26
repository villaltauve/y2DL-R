import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class VistaDescargador:
    def __init__(self, controlador):
        self.controlador = controlador
        self.ventana = tk.Tk()
        self.ventana.title("Descargador de YouTube")
        self.ventana.geometry("500x350")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg="#f0f0f0")

        # Configurar el estilo
        self.configurar_estilo()
        self.crear_componentes()

    def iniciar(self):
        self.ventana.mainloop()

    def configurar_estilo(self):
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10))
        style.configure("TEntry", font=("Arial", 10))

    def crear_componentes(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        ttk.Label(url_frame, text="URL del video:").pack(side=tk.LEFT)
        self.entrada_url = ttk.Entry(url_frame, width=50)
        self.entrada_url.pack(side=tk.LEFT, padx=5)
        ttk.Button(url_frame, text="Pegar", command=self.pegar_url).pack(side=tk.LEFT)

        # Carpeta
        carpeta_frame = ttk.Frame(main_frame)
        carpeta_frame.pack(fill=tk.X, pady=5)
        ttk.Label(carpeta_frame, text="Carpeta de destino:").pack(side=tk.LEFT)
        self.entrada_carpeta = ttk.Entry(carpeta_frame, width=40)
        self.entrada_carpeta.pack(side=tk.LEFT, padx=5)
        ttk.Button(carpeta_frame, text="Elegir carpeta", command=self.controlador.elegir_carpeta).pack(side=tk.LEFT)

        # Resolución
        resolucion_frame = ttk.Frame(main_frame)
        resolucion_frame.pack(fill=tk.X, pady=5)
        ttk.Label(resolucion_frame, text="Resolución:").pack(side=tk.LEFT)
        self.resolucion_var = tk.StringVar(value="720p")
        resoluciones = ["1080p", "720p", "480p", "360p", "240p", "144p"]
        ttk.OptionMenu(resolucion_frame, self.resolucion_var, *resoluciones).pack(side=tk.LEFT, padx=5)

        # Convertir a MP3
        mp3_frame = ttk.Frame(main_frame)
        mp3_frame.pack(fill=tk.X, pady=5)
        self.var_mp3 = tk.BooleanVar()
        ttk.Checkbutton(mp3_frame, text="Convertir a MP3", variable=self.var_mp3).pack(side=tk.LEFT)

        # Botón de descarga
        self.boton_descarga = ttk.Button(main_frame, text="Descargar", command=self.controlador.iniciar_descarga)
        self.boton_descarga.pack(pady=10)

        # Barra de progreso
        self.barra_progreso = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
        self.barra_progreso.pack(pady=10)

        # Mensaje de estado
        self.mensaje_estado = ttk.Label(main_frame, text="")
        self.mensaje_estado.pack(pady=5)

    def pegar_url(self):
        try:
            self.entrada_url.delete(0, tk.END)
            self.entrada_url.insert(0, self.ventana.clipboard_get())
        except:
            pass

    def mostrar_mensaje(self, texto):
        self.mensaje_estado.config(text=texto)
        self.ventana.update()

    def actualizar_barra(self, porcentaje):
        self.barra_progreso["value"] = porcentaje
        self.ventana.update_idletasks()

    def obtener_datos(self):
        return {
            "url": self.entrada_url.get().strip(),
            "carpeta": self.entrada_carpeta.get(),
            "resolucion": self.resolucion_var.get(),
            "convertir_mp3": self.var_mp3.get()
        }

    def set_carpeta(self, carpeta):
        self.entrada_carpeta.delete(0, tk.END)
        self.entrada_carpeta.insert(0, carpeta)

    def deshabilitar_boton(self):
        self.boton_descarga.config(state="disabled")

    def habilitar_boton(self):
        self.boton_descarga.config(state="normal")
