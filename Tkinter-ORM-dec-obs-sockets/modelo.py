# from ast import Pass
from fileinput import close
from mensajes import Vmensajes
# from http.client import NOT_MODIFIED
from tkinter import Tk
from unittest import load_tests
from warnings import showwarning
import sqlite3
import mysql.connector
import re
from tkinter import ttk
from modregex import Textofiltro
import shelve
from peewee import *
from decoradores import decorador_insertar
from observador import Sujeto

# HACER UN CAMPOR xxxx QUE VALIDE SOLO ALFANUMERICOS
# : patron="^[A-Za-z]+(?:[ _-][A-Za-z]+)*$".
# trabajo final hay q hacer un ORM.


##############################
# MODELO
###############################

sqlite3db = SqliteDatabase("mibase.db")
# mysql_db = MySQLDatabase('my_app', user='app', password='db_password',
#  host='10.1.0.8', port=3306)

try:
    class BaseModel(Model):
        class Meta:
            database = sqlite3db

    class Stock(BaseModel):
        _nroparte_var = CharField()
        _cantidad_var = IntegerField()
        _lote_var = CharField()
        _descripcion_var = CharField()

    # objStock=Stock()
except:
    print("error")


class Orm():
    def connection():
        sqlite3db.connect()

    def createTable():
        sqlite3db.create_tables([Stock])

##############################
# MODELO
###############################


class Database():
    def __init__(self,):
        Orm.connection()
        Orm.createTable()
        self.objvmensaje = Vmensajes()


class Abmc(Database, Sujeto):
    def __init__(self, ):

        self.objStock = Stock()  # Creo el objeto
        self.objvmensaje = Vmensajes()
        self.objmodregex = Textofiltro()

    def conexion_db(self, base):
        if base == 'mysql':
            sqlite3db.close()
            try:
                self.mibase_ = self.database_.conexion_db_mysql()
            except:
                pass
            try:
                self.micursor = self.mibase_.cursor()
                self.micursor.execute("CREATE DATABASE "+self.nomdb)
            except:
                pass

        elif base == 'sqlite3':
            try:
                Orm.connection()
            except:
                pass

    def crear_tabla(self, base):

        if base == 'mysql':
            sqlite3db.close()
            try:
                micursor = self.mibase_.cursor()
                self.database_.make_table_db_mysql(micursor)
            except:
                self.objvmensaje.mensajeerrordb(3)

        elif base == 'sqlite3':
            try:
                Orm.createTable()
            except:
                pass

            return

    def _borrar(self, id_var, nroparte_var, cantidad_var, lote_var, descripcion_var, tree):

        var_conf = self.objvmensaje.notificacion(2)
        if not var_conf:
            return
        item_selected = tree.focus()
        # print(item_selected)
        valor_id = tree.item(item_selected)
        # print(valor_id)
        # print(valor_id['text'])
        # borrar = self.objStock.get(self.objStock.id == valor_id['text'])

        borrar = Stock.get(Stock.id == valor_id['text'])
        # print(borrar)
        borrar.delete_instance()
        # self.objvmensaje.mensaje_campo_malingresado(4)

        self.actualizar_treeview(tree)

        try:
            self.datos_log("Insert", nroparte_var.get(
            ), cantidad_var.get(), lote_var.get(), descripcion_var.get())
            # observador
            self.notificar("ClassAbmc Method insertar- params", nroparte_var.get(),
                           cantidad_var.get(), lote_var.get(), descripcion_var.get())
        except:
            print("error log and observador")
        self.borrar_entrys(id_var, nroparte_var, cantidad_var,
                           lote_var, descripcion_var)

        return

    def _modificar(self, id_var, nroparte_var, cantidad_var, lote_var, descripcion_var, tree):

        item_seleccionado = tree.focus()
        valor_id = tree.item(item_seleccionado)
        actualizar = Stock.update(
            _nroparte_var=nroparte_var.get(), _descripcion_var=descripcion_var.get(), _lote_var=lote_var.get(), _cantidad_var=cantidad_var.get()
        ).where(Stock.id == valor_id["text"])

        try:
            self.datos_log("Insert", nroparte_var.get(
            ), cantidad_var.get(), lote_var.get(), descripcion_var.get())
            # observador
            self.notificar("ClassAbmc Method insertar- params", nroparte_var.get(),
                           cantidad_var.get(), lote_var.get(), descripcion_var.get())
        except:
            print("error log and observador")

        actualizar.execute()
        self.actualizar_treeview(tree)

    def _seleccionar(self, id_var, nroparte_var, cantidad_var, lote_var, descripcion_var, tree):
        item_seleccionado = tree.focus()
        valor_id = tree.item(item_seleccionado)
        try:
            id_var.set(Stock.get(Stock.id == valor_id['text']))
            nroparte_var.set(
                Stock.get(Stock.id == valor_id['text'])._nroparte_var)
            cantidad_var.set(
                Stock.get(Stock.id == valor_id['text'])._cantidad_var)
            lote_var.set(Stock.get(Stock.id == valor_id['text'])._lote_var)
            descripcion_var.set(
                Stock.get(Stock.id == valor_id['text'])._descripcion_var)
        except:
            self.objvmensaje.mensaje_campo_malingresado(4)
            return
        return

    def _insertar(self, id_var, nroparte_var, cantidad_var, lote_var, descripcion_var, tree):

        self.objStock._nroparte_var = nroparte_var.get()
        self.objStock._cantidad_var = cantidad_var.get()
        self.objStock._lote_var = lote_var.get()
        self.objStock._descripcion_var = descripcion_var.get()

        # #modulo modregex clase Textofiltro metodo filtronumerico
        resultado = self.objmodregex.filtro_numero(cantidad_var.get())
        resultado1 = self.objmodregex.filtro_cadena(descripcion_var.get())

        if not resultado1:
            self.objvmensaje.mensaje_campo_malingresado(6)
            return

        if not resultado:
            self.objvmensaje.mensaje_campo_malingresado(1)
            return
        else:  # si resultado correcto
            if (self.objStock._nroparte_var == "" or self.objStock._nroparte_var == "" or self.objStock._cantidad_var == "" or self.objStock._lote_var == "" or self.objStock._descripcion_var == ""):
                self.objvmensaje.mensaje_campo_malingresado(2)
                return
            pass

        self.objStock.save()
        try:
            self.datos_log("Insert", nroparte_var.get(
            ), cantidad_var.get(), lote_var.get(), descripcion_var.get())
            # observador
            self.notificar("ClassAbmc Method insertar- params", nroparte_var.get(),
                           cantidad_var.get(), lote_var.get(), descripcion_var.get())
        except:
            print("error log and observador")

        self.actualizar_treeview(tree)
        self.objvmensaje.notificacion(1)
        self.borrar_entrys(id_var, nroparte_var, cantidad_var,
                           lote_var, descripcion_var)
        return

    def actualizar_treeview(self, mitreview):
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        for valor_recuperado in self.objStock.select():
            # print(valor_recuperado)
            mitreview.insert("", 0, text=valor_recuperado.id, values=(valor_recuperado._nroparte_var,
                             valor_recuperado._cantidad_var, valor_recuperado._lote_var, valor_recuperado._descripcion_var), tags=("odd",),)
        return

    def _ver_db(self, tree):
        self.actualizar_treeview(tree)
        return

    def borrar_entrys(self, id_var, nroparte_var, cantidad_var, lote_var, descripcion_var):
        id_var.set("")
        nroparte_var.set("")
        cantidad_var.set("")
        lote_var.set("")
        descripcion_var.set("")
        return

    @decorador_insertar
    def datos_log(self, tipo, b, c, d, f):
        pass
