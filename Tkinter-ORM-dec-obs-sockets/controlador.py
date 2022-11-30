from tkinter import Tk
import vista
import observador

# ##############################################
# CONTROLADOR
# ##############################################

class Controlador():
    def __init__(self,ventana):
        self.ventana=ventana
        self.objeto_vista=vista.Vistaprincipal(self.ventana)
        self.observador1=observador.ConcreteObserver(self.objeto_vista.objcontr)

if __name__=="__main__":
    main=Tk()
    Controlador(main)
    main.mainloop()
