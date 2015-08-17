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
    lista_archivo = []
    # Lista ficheros
    lista_directorio = os.walk(path)

    # Crea lista con los archivos encontrados en la carpeta Data_xml
    for root, dirs, files in lista_directorio:
        for fichero in files:
            (nombre_fichero, extension) = os.path.splitext(fichero)
            if(extension == ".xml"):
                lista_archivo.append(nombre_fichero+extension)

    return lista_archivo


def cargar_datos_db(db, datos):
    with db.cursor() as cursor:
        for dato in datos:
            fecha = dato['fecha']
            valor = float(dato['valor'].replace(',', '.'))
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

    lista = listar_archivos()
    for archivo in lista:
        datos = cargar_archivo('Data_xml/' + archivo)
        cargar_datos_db(connection, datos)


if __name__ == '__main__':
        main()
