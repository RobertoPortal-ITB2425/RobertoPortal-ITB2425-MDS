import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Cambia la ruta a tu archivo CSV aquí
csv_file = 'TA03_v1.csv'  # Asegúrate de que esta ruta sea correcta

# Crear la raíz del documento XML
root = ET.Element('Datos')

# Abrir el archivo CSV y leer su contenido
try:
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        # Iterar sobre las filas del CSV y añadirlas al XML
        for row in csv_reader:
            item = ET.SubElement(root, 'Incidencia')
            for key, value in row.items():
                sanitized_key = key.replace(" ", "_")  # Reemplazar espacios por guiones bajos
                child = ET.SubElement(item, sanitized_key)
                child.text = str(value)

    # Crear el árbol XML
    tree = ET.ElementTree(root)

    # Convertir a un string con formato
    xml_string = ET.tostring(root, encoding='utf-8')
    print(xml_string.decode('utf-8'))  # Imprimir el XML generado

    parsed_xml = minidom.parseString(xml_string)
    pretty_xml = parsed_xml.toprettyxml(indent="    ")

    # Guardar el archivo XML
    xml_file = 'TA03_v1.xml'
    with open(xml_file, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

    print(f'Archivo XML guardado como {xml_file}')

except FileNotFoundError:
    print(f"Error: No se encontró el archivo: {csv_file}")
