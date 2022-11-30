

from tkinter import DISABLED
from tkinter import Tk
from tkinter import E
from tkinter import W
from tkinter import Menu
from tkinter import Label
from tkinter import IntVar
from tkinter import Button
from tkinter import Entry
from tkinter import StringVar
from tkinter import ttk
import modelo
from mensajes import Vmensajes

# #############################################
# VISUAL
# #############################################


class Vistaprincipal():
    
    def __init__(self,miventana):
        
        self.objcontr=modelo.Abmc()
        
        self.ventana= miventana
        self.ventana.title("Incoming Material - UTN Python")
        self.ventana.geometry("900x400")
        self.menubar=Menu(self.ventana)
        self.menubararch=Menu(self.menubar,tearoff=0)

        self.menubararch.add_command(label="Salir", command=self.ventana.quit)
        self.menubar.add_cascade(label="Archivo", menu=self.menubararch)

        Label(self.ventana,text="id").grid(row=0,column=0,sticky=W)
        Label(self.ventana, text="Nro Parte").grid(row=1,column=0,sticky=W)
        Label(self.ventana, text="Cantidad").grid(row=2,column=0,sticky=W)
        Label(self.ventana, text="Lote").grid(row=3,column=0,sticky=W)
        Label(self.ventana, text="Descripcion").grid(row=1,column=2,sticky=W)
        Label(self.ventana, text="Base de datos").grid(row=2,column=2,sticky=W)
        
        self.id_var=IntVar()
        self.nroparte_var=StringVar()
        self.cantidad_var=StringVar()
        self.lote_var=StringVar()
        self.descripcion_var=StringVar()
        # self.strbd=StringVar()
        # self.strtabla=StringVar()
        # self.strbd="mi_db"
        # self.strtabla="stockinicial"
        
    
        self.id=Entry(self.ventana,textvariable=self.id_var,state=DISABLED)
        self.nroparte=Entry(self.ventana,textvariable=self.nroparte_var)
        self.cantidad=Entry(self.ventana,textvariable=self.cantidad_var)
        self.lote=Entry(self.ventana,textvariable=self.lote_var)
        self.descripcion=Entry(self.ventana,textvariable=self.descripcion_var)
        # self.bd=Entry(self.ventana,textvariable=self.strbd)
        # self.tabla=Entry(self.ventana,textvariable=self.strtabla)


        self.id.grid(row=0,column=1)
        self.nroparte.grid(row=1,column=1)
        self.cantidad.grid(row=2,column=1)
        self.lote.grid(row=3,column=1)
        self.descripcion.grid(row=1,column=3)
        # self.bd.grid(row=2,column=3)
        # self.tabla.grid(row=3,column=3)
        # llamo a la funcion q crea el combobox
        self.valorcombobox()
        # # --------------------------------------------------
        # TREEVIEW
        # --------------------------------------------------

        self.tree = ttk.Treeview(self.ventana)
        self.tree["columns"]=("col1", "col2", "col3", "col4")
        self.tree.column("#0", width=90, minwidth=50, anchor=W)
        self.tree.column("col1", width=200, minwidth=80)
        self.tree.column("col2", width=200, minwidth=80)
        self.tree.column("col3", width=200, minwidth=80)
        self.tree.column("col4", width=200, minwidth=80)
        self.tree.heading("#0", text="ID")
        self.tree.heading("col1", text="Nro de Parte")
        self.tree.heading("col2", text="Cantidad")
        self.tree.heading("col3", text="Lote")
        self.tree.heading("col4", text="Descripcion")
        self.tree.grid(row=10, column=0,columnspan=4,sticky=W+E)
        
        
        self.bi=Button(self.ventana,text= "Insertar",command=lambda:self.objcontr._insertar(self.id_var  ,self.nroparte_var  ,self.cantidad_var  ,self.lote_var  ,self.descripcion_var,self.tree)).grid(row=5,column=0)
        self.bb=Button(self.ventana,text= "Borrar",command=lambda:self.objcontr._borrar(self.id_var,self.nroparte_var  ,self.cantidad_var  ,self.lote_var  ,self.descripcion_var,self.tree)).grid(row=5,column=1)
        self.bm=Button(self.ventana,text= "Modificar",command=lambda:self.objcontr._modificar(self.id_var,self.nroparte_var,self.cantidad_var,self.lote_var,self.descripcion_var,self.tree)).grid(row=5,column=2)
        self.bs=Button(self.ventana,text= "Seleccionar",command=lambda:self.objcontr._seleccionar(self.id_var,self.nroparte_var,self.cantidad_var,self.lote_var,self.descripcion_var,self.tree)).grid(row=5,column=3)
        self.bvd=Button(self.ventana,text= "Ver DB",command=lambda:self.objcontr._ver_db(self.tree)).grid(row=4,column=3)
        # self.bbd=Button(self.ventana,text= "DB Aceptar",command=lambda:self.objcontr._ver_db(self.tree)).grid(row=4,column=2)
        return
    
    def valorcombobox(self,):
        self.valorcom=StringVar()
        self.valorcom.trace('w',self.eleccion)
        self.combo1=ttk.Combobox(self.ventana,textvariable=self.valorcom)
        self.combo1['values']=('sqlite3','mysql','mongodb','shelve')
        self.combo1.set('sqlite3')
        self.combo1.grid(row=2,column=3) 
        return
 
    def eleccion(self, *args):
        try:
            print(self.combo1.get()) 
            self.objcontr.conexion_db(self.combo1.get())
            self.objcontr.crear_tabla(self.combo1.get())
        except ValueError:
            print("error")
            # Vmensajes.mensajeerrordb(1)
