#!/usr/bin/python
# -*- coding: utf-8

import os
import sys
import argparse
import pymysql.cursors
import xml.etree.ElementTree as ET


def cargar_archivo(archivo):
    ns = {'src': 'http://api.sbif.cl'}
    arbol = ET.parse(archivo)
    dolares = arbol.findall('src:Dolares', ns)[0].findall('src:Dolar', ns)

    for dolar in dolares:
        yield {'fecha': dolar.find('src:Fecha', ns).text,
               'valor': dolar.find('src:Valor', ns).text}


def listar_archivos():
    path = os.getcwd() + '/Data_xml'
    # Lista ficheros
    lista_directorio = os.walk(path)

    # Crea lista con los archivos encontrados en la carpeta Data_xml
    for root, dirs, files in lista_directorio:
        for fichero in files:
            (nombre_fichero, extension) = os.path.splitext(fichero)
            if(extension == ".xml"):
                yield nombre_fichero + extension


# esta clase se encarga de realizar todas las operaciones 
# relacionadas a la base de datos
class Db:
    def __init__(self, connection):
        self.connection = connection

    # Este metodo recibe una lista de
    # diccionarios {valor, dato}
    # y los almacena en la db
    # actualizando i insertando datos segun corresponda
    def cargar_datos(self, datos):
        for dato in datos:
            fecha = dato['fecha']
            valor = float(dato['valor'].replace(',', '.'))

            if len(self.buscar_fecha(fecha)) > 0:
                self.actualizar_fecha(fecha, valor)
            else:
                self.agregar_fecha(fecha, valor)
                
    def actualizar_fecha(self, fecha, valor):
        sql = 'call actualizar_fecha(%s, %s)'
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (fecha, valor))
    
    def agregar_fecha(self, fecha, valor):
        sql = 'call agregar_fecha(%s, %s)'
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (fecha, valor))

    def buscar_fecha(self, fecha):
        sql = 'call buscar_fecha(%s)'
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (fecha))
            return cursor.fetchall()

    # hay que llamar a este metodo
    # para realizar los cambios en la base de datos
    def commit(self):
        self.connection.commit()
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user',
                        help="Nombre del usuario de la base de datos")
    parser.add_argument('-p', '--password',
                        help="Contraseña del usuario de la base de datos")

    arg = parser.parse_args()

    if not (arg.user and arg.password):
        print("Necesito un usuario y contraseña")
        sys.exit(-1)

    connection = pymysql.connect(host='localhost',
                                 user=arg.user,
                                 password=arg.password,
                                 db='Divisas')

    db = Db(connection)
    lista = listar_archivos()
    for archivo in lista:
        datos = cargar_archivo('Data_xml/' + archivo)
        db.cargar_datos(datos)
    db.commit()


if __name__ == '__main__':
        main()
