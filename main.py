from controlador import Controlador
from vista import VistaDescargador

if __name__ == "__main__":
    controlador = Controlador()
    vista = VistaDescargador(controlador)
    controlador.set_vista(vista)
    vista.iniciar()
