import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Cargar y parsear el archivo XML original
tree = ET.parse('TA03.xml')
root = tree.getroot()

# Crear el nuevo árbol XML
data = ET.Element('data')

# Iterar sobre cada entrada <row> en el archivo XML original
for row in root.findall('row'):
    # Crear el nuevo elemento <incidencia>
    incidencia = ET.SubElement(data, 'incidencia')
    incidencia.set('nombre', row.find('NOMBRES_Y_APELLIDOS').text)

    # Añadir los elementos hijos con sus respectivos datos
    ET.SubElement(incidencia, 'codigo').text = row.find('CÓDIGO_DE_ESTUDIANTE').text
    ET.SubElement(incidencia, 'fecha').text = row.find('FECHA_EN_LA_QUE_OCURRIÓ_POR_PRIMERA_VEZ').text
    ET.SubElement(incidencia, 'aula').text = row.find('AULA_SALA').text
    ET.SubElement(incidencia, 'tipo').text = row.find('TIPO_DE_INCIDENCIA').text
    ET.SubElement(incidencia, 'detalle').text = row.find('DETALLE_DE_LA_INCIDENCIA').text
    ET.SubElement(incidencia, 'equipo').text = row.find('EQUIPOS_y_o_SERVICIOS_AFECTADOS').text
    ET.SubElement(incidencia, 'descripcion').text = row.find('DESCRIPCIÓN_BREVE').text
    ET.SubElement(incidencia, 'urgencia').text = row.find('NIVEL_DE_URGENCIA').text

# Convertir el árbol XML en una cadena con formato
xml_str = ET.tostring(data, encoding='utf-8')
parsed_xml = minidom.parseString(xml_str)
formatted_xml = parsed_xml.toprettyxml(indent="    ")

# Guardar el XML formateado en un archivo
with open('resultado_formateado.xml', 'w', encoding='utf-8') as f:
    f.write(formatted_xml)

print("Transformación completada. Archivo guardado como 'resultado_formateado.xml'.")