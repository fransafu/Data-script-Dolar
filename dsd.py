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

print(cargar_archivo(sys.argv[1]))
