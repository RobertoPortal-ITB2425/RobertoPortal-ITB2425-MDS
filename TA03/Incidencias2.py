import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse("TA03.xml")
root = tree.getroot()

root.tag
"row"
root.attrib
{}
cont =0
fecha_inicio = datetime.strptime("08/10/2024", "%d/%m/%Y")
fecha_fin = datetime.strptime("31/10/2024","%d/%m/%Y")
contador=0

for child in root:
    cont= cont+1
print(f"Total de inciencias: {cont}")

for row in root.findall("row"):
    marca_de_temps = row.find("Marca_de_temps")
    if marca_de_temps is not None:
        fecha_hora_str = marca_de_temps.text
        fecha_hora = datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M:%S")
        if fecha_inicio <= fecha_hora <= fecha_fin:
            contador += 1
print(f"Total de incidencias en fecha: {contador}")