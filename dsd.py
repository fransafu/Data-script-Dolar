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

    return [{'fecha': d.find('src:Fecha', ns).text,
             'valor': d.find('src:Valor', ns).text}
            for d in dolares]


def listaArchivos():
    path = os.getcwd() + '/Data_xml'
    listaArchivo = []
    # Lista ficheros
    listaDirectorio = os.walk(path)

    # Crea lista con los archivos encontrados en la carpeta Data_xml
    for root, dirs, files in listaDirectorio:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if(extension == ".xml"):
                listaArchivo.append(nombreFichero+extension)

    return listaArchivo


def cargar_datos_db(db, datos):
    with db.cursor() as cursor:
        for dato in datos:
            fecha = dato['fecha']
            valor = dato['valor']
            sql = 'INSERT INTO `Dolar` (`Fecha`, `Valor`) VALUES (%s, %s)'
            cursor.execute(sql, (fecha, valor))
            db.commit()


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

    lista = listaArchivos()
    for archivo in lista:
        datos = cargar_archivo('Data_xml/' + archivo)
        cargar_datos_db(connection, datos)


if __name__ == '__main__':
        main()
