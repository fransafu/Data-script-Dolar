#!/usr/bin/python
# -*- coding: utf-8

import os
import sys
import xml.etree.ElementTree as ET


def cargar_archivo(archivo):
    ns = {'src': 'http://api.sbif.cl'}
    arbol = ET.parse(archivo)
    dolares = arbol.findall('src:Dolares', ns)[0].findall('src:Dolar', ns)

    resultado = []
    for dolar in dolares:
        fecha = dolar.find('src:Fecha', ns).text
        valor = dolar.find('src:Valor', ns).text
        resultado.append({'fecha': fecha,
                          'valor': valor})

    return resultado

def listaArchivos():
    path = os.getcwd() + '/Data_xml'
    listaArchivo = []
    listaDirectorio = os.walk(path) # Lista ficheros

    # Crea lista con los archivos encontrados en la carpeta Data_xml
    for root, dirs, files in listaDirectorio:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if(extension == ".xml"):
                listaArchivo.append(nombreFichero+extension)

    return listaArchivo

def main():
    lista = listaArchivos()
    for archivo in lista:
        for dato in cargar_archivo('Data_xml/' + archivo):
            print dato

if __name__ == "__main__":
    main()