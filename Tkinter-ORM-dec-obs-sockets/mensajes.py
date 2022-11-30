from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno

class Vmensajes():

    def mensajeerrordb(self,nro):

        if int(nro)==1:
            showerror("Error DB","Error de CONEXION")
        if int(nro)==2:
            showerror("Error DB","Error de al crear BASE DE DATOS")
        if int(nro)==3:
            showerror("Error DB","Error de al crear TABLA")
        return
    
    def mensaje_campo_malingresado(self,nro):
        if int(nro)==1:
            showerror("Advertencia","Solo poner numeros en el campo de cantidad")
        if int(nro)==2:
            showerror("Advertencia","Datos vacios en los campos/datos incorrectos")
        if int(nro)==3:
            showerror("Error DB","Error de al crear TABLA")
        if int(nro)==4:
            showerror("Advertencia","No hay ningun campo seleccionado")
        if int(nro)==5:
            showerror("Advertencia","No hay campo para borrar")
        if int(nro)==6:
            showerror("Advertencia","Solo poner texto")
        return
        
    def notificacion(self,nro):
        if int(nro)==1:
            showinfo("Info","Se ingresaron datos en la BD")
        if int(nro)==2:
            return askyesno("Confirmacion","Seguro quiere Borrar los datos")
        if int(nro)==3:
            showinfo("Modificado","Se modificaron los datos en la TABLA")
        return

    def mensajeerror(self,):
        showerror("Error A0","Error de datos")
        return