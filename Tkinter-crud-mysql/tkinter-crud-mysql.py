from http.client import NOT_MODIFIED
from tkinter import *
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from tkinter.messagebox import askyesno
from unittest import load_tests
from warnings import showwarning
import mysql.connector
import re
from tkinter import ttk

# ##############################################
# MODELO
# ##############################################

nomtabla="stockinicial"
nomdb="mi_db"
mibase=""
bm=""

def mensajeerrordb(nro):
   ''' if int(nro)==1:
        showerror("Error DB","Error de CONEXION")
    if int(nro)==2:
        showerror("Error DB","Error de al crear BASE DE DATOS")
    if int(nro)==3:
        showerror("Error DB","Error de al crear TABLA")
    return
    '''
def mensaje_campo_malingresado(nro):
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
    
    return
    
def notificacion(nro):
    if int(nro)==1:
        showinfo("Info","Se ingresaron datos en la BD")
    if int(nro)==2:
        return askyesno("Confirmacion","Seguro quiere Borrar los datos")
    if int(nro)==3:
        showinfo("Modificado","Se modificaron los datos en la TABLA")
    return




def conexion_db(nomdb):
    try:
        mibase_ = mysql.connector.connect(host="localhost", user="root", passwd="",database=nomdb)
    except:
        mensajeerrordb(1)

    return mibase_

def crear_db(mibase_,nomdb):
    try:
        micursor = mibase_.cursor()
        micursor.execute("CREATE DATABASE "+nomdb)
    except:
        mensajeerrordb(2)

    return

def crear_tabla(mibase_,nomtabla):
    try:
        micursor = mibase_.cursor()
        sql = "CREATE TABLE " +nomtabla+ " (id int(10) NOT NULL PRIMARY KEY AUTO_INCREMENT, nro_parte VARCHAR(20) COLLATE utf8_spanish2_ci,cantidad VARCHAR(10) COLLATE utf8_spanish2_ci ,lote VARCHAR(20) COLLATE utf8_spanish2_ci, descripcion VARCHAR(20) COLLATE utf8_spanish2_ci)"
        micursor.execute(sql)
        mibase_.commit()#guarda los cambios
    except:
        mensajeerrordb(3)
    return

def inicio():
    mibase_=conexion_db("") #me conecto a mysql
    crear_db(mibase_,nomdb) # creo una base de datos. 
    mibase_=conexion_db(nomdb) # me conecto a la base de datos mi_db
    crear_tabla(mibase_,nomtabla)
    return mibase_

def mensajeerror():
    showerror("Error A0","Error de datos")
    return

def borrar_entrys():
    id_var.set("")
    nroparte_var.set("")
    cantidad_var.set("")
    lote_var.set("")
    descripcion_var.set("")
    return

def boton_insertar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var):
    global nomtabla
    global nomdb
    global mibase
    datos = (nroparte_var.get(),cantidad_var.get(),lote_var.get(),descripcion_var.get())  
    patron=re.compile(r'[0-9][0-9]{0,6}',re.X)
    resultado=patron.match(str(datos[1]))
        
    if not resultado:
        mensaje_campo_malingresado(1)
        return
    else:#si resultado correcto
        for n in datos:
            if n=="":
                mensaje_campo_malingresado(2)
                return
    
    
    micursor = mibase.cursor()
    sql = "INSERT INTO "+nomtabla+" (nro_parte, cantidad, lote, descripcion) VALUES (%s, %s, %s, %s)"
    micursor.execute(sql, datos)
    mibase.commit() #guarda los cambios
    print("Estoy en alta todo ok")
    actualizar_treeview(tree)
    borrar_entrys() 
    notificacion(1)
    return

def boton_borrar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var):
    global nomtabla
    global nomdb
    global mibase
    var_conf=notificacion(2)
    if not var_conf:
        return
        
    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item['text']
    micursor = mibase.cursor()
    data = (mi_id,)
    sql = "DELETE FROM "+nomtabla+" WHERE id=%s"
    micursor.execute(sql, data)
    mibase.commit()
    try:
        tree.delete(valor)
    except:
        mensaje_campo_malingresado(4)
    borrar_entrys()
    return
    
    
def boton_modificar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var):
    global nomdb
    global nomtabla
    global mibase
    micursor = mibase.cursor()
    sql = "UPDATE "+nomtabla+" SET nro_parte=%s, cantidad=%s, lote=%s,descripcion=%s WHERE id=%s"
    try:
        datos=(nroparte_var.get(),cantidad_var.get(),lote_var.get(),descripcion_var.get(),id_var.get())
    except:
        mensaje_campo_malingresado(4)
        return
    micursor.execute(sql,datos)
    mibase.commit()
    actualizar_treeview(tree)
    borrar_entrys()
    return

def boton_seleccionar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var):
    global nomdb
    global nomtabla
    global mibase
    global bm

    valor = tree.selection()
    item = tree.item(valor)
    mi_id = item['text']
    micursor = mibase.cursor()
    sql = "SELECT * FROM "+nomtabla+" WHERE id=%s"
    datos=(mi_id,)
    micursor.execute(sql,datos)
    resultado = micursor.fetchall()
    try:
        id_var.set(resultado[0][0])
        nroparte_var.set(resultado[0][1])
        cantidad_var.set(resultado[0][2])
        lote_var.set(resultado[0][3])
        descripcion_var.set(resultado[0][4])
    except:
        mensaje_campo_malingresado(4)
        return
    return

  
  
def actualizar_treeview(mitreview):
    global nomdb
    global nomtabla
    global mibase
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)
    micursor = mibase.cursor()
    sql = "SELECT * FROM "+nomtabla+" ORDER BY id ASC"
    micursor.execute(sql)
    resultado = micursor.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3],fila[4]))
    return


def ver_db():
    actualizar_treeview(tree)
    return

mibase=inicio()#se conecta, genera la bd mi_db y crea la tabla stockinicial

ventana=Tk()

# ##############################################
# VISUAL
# ##############################################

ventana.title("Incoming Material - UTN Python")
ventana.geometry("900x400")
menubar=Menu(ventana)
menubararch=Menu(menubar,tearoff=0)

menubararch.add_command(label="Salir", command=ventana.quit)
menubar.add_cascade(label="Archivo", menu=menubararch)

idl=Label(ventana,text="id").grid(row=0,column=0,sticky=W)
Label(ventana, text="Nro Parte").grid(row=1,column=0,sticky=W)
Label(ventana, text="Cantidad").grid(row=2,column=0,sticky=W)
Label(ventana, text="Lote").grid(row=3,column=0,sticky=W)
Label(ventana, text="Descripcion").grid(row=1,column=2,sticky=W)

id_var=IntVar()
nroparte_var=StringVar()
cantidad_var=StringVar()
lote_var=StringVar()
descripcion_var=StringVar()

id=Entry(ventana,textvariable=id_var,state=DISABLED)
nroparte=Entry(ventana,textvariable=nroparte_var)
cantidad=Entry(ventana,textvariable=cantidad_var)
lote=Entry(ventana,textvariable=lote_var)
descripcion=Entry(ventana,textvariable=descripcion_var)

id.grid(row=0,column=1)
nroparte.grid(row=1,column=1)
cantidad.grid(row=2,column=1)
lote.grid(row=3,column=1)
descripcion.grid(row=1,column=3)

borrar_entrys()

# --------------------------------------------------
# TREEVIEW
# --------------------------------------------------

tree = ttk.Treeview(ventana)
tree["columns"]=("col1", "col2", "col3", "col4")
tree.column("#0", width=90, minwidth=50, anchor=W)
tree.column("col1", width=200, minwidth=80)
tree.column("col2", width=200, minwidth=80)
tree.column("col3", width=200, minwidth=80)
tree.column("col4", width=200, minwidth=80)
tree.heading("#0", text="ID")
tree.heading("col1", text="Nro de Parte")
tree.heading("col2", text="Cantidad")
tree.heading("col3", text="Lote")
tree.heading("col4", text="Descripcion")
tree.grid(row=10, column=0,columnspan=4,sticky=W+E)

bi=Button(ventana,text= "Insertar",command=lambda:boton_insertar(id_var  ,nroparte_var  ,cantidad_var  ,lote_var  ,descripcion_var  )).grid(row=5,column=0)
bb=Button(ventana,text= "Borrar",command=lambda:boton_borrar(id_var,nroparte_var  ,cantidad_var  ,lote_var  ,descripcion_var  )).grid(row=5,column=1)
bm=Button(ventana,text= "Modificar",command=lambda:boton_modificar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var)).grid(row=5,column=2)
bs=Button(ventana,text= "Seleccionar",command=lambda:boton_seleccionar(id_var,nroparte_var,cantidad_var,lote_var,descripcion_var)).grid(row=5,column=3)
bs=Button(ventana,text= "Ver DB",command=lambda:ver_db()).grid(row=4,column=3)


mainloop()
