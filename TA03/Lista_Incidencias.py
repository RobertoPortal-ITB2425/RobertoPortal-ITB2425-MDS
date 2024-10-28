import xml.etree.ElementTree as ET

def extraer_incidencias(xml_file):
    # Cargar y parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Inicializar lista de incidencias
    lista_incidencias = []

    # Iterar sobre cada incidencia en el XML
    for incidencia in root.findall('Incidencia'):
        # Crear un diccionario para almacenar la información de la incidencia
        incidencia_data = {}
        for elemento in incidencia:
            # Guardar los datos de cada elemento en el diccionario
            incidencia_data[elemento.tag] = elemento.text

        # Añadir la incidencia completa a la lista de incidencias
        lista_incidencias.append(incidencia_data)

    return lista_incidencias

# Ruta del archivo XML
ruta_archivo_xml ='TA03.xml'  # Cambia esto por la ruta de tu archivo

# Llama a la función y obtiene la lista de incidencias
incidencias = extraer_incidencias(ruta_archivo_xml)

# Imprimir la lista de incidencias
for i, inc in enumerate(incidencias, start=1):
    print(f'Incidencia {i}:')
    for key, value in inc.items():
        print(f'  {key}: {value}')
    print()