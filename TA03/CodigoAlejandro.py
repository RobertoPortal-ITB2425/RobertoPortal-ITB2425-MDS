import xml.etree.ElementTree as ET
import json
from datetime import datetime


def validar_fecha(fecha_str):
    """Valida que la fecha esté en formato YYYY-MM-DD."""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def extraer_incidencias(xml_file):
    # Cargar y parsear el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Espacio de nombres en XML
    ns = {'ns1': 'http://www.exemple.com/IncidenciasGrup4'}

    # Inicializar listas
    lista_todas_incidencias = []  # Lista para almacenar todas las incidencias
    lista_incidencias_validas = []  # Lista para almacenar las incidencias válidas
    lista_incidencias_erroneas = []  # Lista para almacenar las incidencias erróneas
    incidencias_molt_urgent = 0  # Contador para incidencias "Molt Urgent"

    # Obtener la fecha actual
    fecha_actual = datetime.today().date()

    # Definir las fechas clave
    fecha_septiembre_actual = datetime(year=fecha_actual.year, month=9, day=1).date()
    fecha_diciembre_actual = datetime(year=fecha_actual.year, month=12, day=31).date()
    fecha_junio_siguiente = datetime(year=fecha_actual.year + 1, month=6, day=30).date()

    # Estamos entre septiembre y diciembre del año actual
    if fecha_actual.month >= 9:
        fecha_inicio_valida = fecha_septiembre_actual
        fecha_fin_valida = fecha_actual
    else:
        fecha_inicio_valida = fecha_septiembre_actual.replace(year=fecha_actual.year - 1)
        fecha_fin_valida = fecha_actual

    # Iterar sobre cada incidencia en el XML
    for incidencia in root.findall('.//ns1:Incidencia', ns):
        # Extraer todos los elementos de la incidencia
        incidencia_data = {}
        for elemento in incidencia:
            # Guardar los datos de cada elemento en un diccionario
            incidencia_data[elemento.tag.split('}')[1]] = elemento.text

        # Añadir la incidencia completa a la lista de todas las incidencias
        lista_todas_incidencias.append(incidencia_data)

        # Validar la fecha de la incidencia
        if 'DataIncidencia' in incidencia_data and validar_fecha(incidencia_data['DataIncidencia']):
            fecha_incidencia = datetime.strptime(incidencia_data['DataIncidencia'], "%Y-%m-%d").date()

            # Verificar si la fecha de incidencia es válida (dentro del rango adecuado)
            if fecha_inicio_valida <= fecha_incidencia <= fecha_fin_valida:
                lista_incidencias_validas.append(incidencia_data)

                # Contar cuántas incidencias tienen nivel de urgencia "Molt Urgent"
                if incidencia_data.get('NivellUrgencia') == "Molt Urgent":
                    incidencias_molt_urgent += 1
            else:
                # Si la fecha está fuera del rango válido, es errónea
                lista_incidencias_erroneas.append(incidencia_data)

    # Generar el nombre del archivo JSON con la fecha actual
    nombre_archivo_json_validas = f'incidencias_validas_{fecha_actual}.json'
    nombre_archivo_json_erroneas = f'incidencias_erroneas_{fecha_actual}.json'

    # Guardar las incidencias válidas en un archivo .json
    with open(nombre_archivo_json_validas, 'w', encoding='utf-8') as f:
        json.dump(lista_incidencias_validas, f, ensure_ascii=False, indent=4)

    # Guardar las incidencias erróneas en un archivo .json
    with open(nombre_archivo_json_erroneas, 'w', encoding='utf-8') as f:
        json.dump(lista_incidencias_erroneas, f, ensure_ascii=False, indent=4)

    # Calcular el porcentaje de incidencias "Molt Urgent"
    porcentaje_molt_urgent = 0
    if len(lista_incidencias_validas) > 0:
        porcentaje_molt_urgent = (incidencias_molt_urgent / len(lista_incidencias_validas)) * 100

    # Imprimir resultados
    print(f'Total de incidencias encontradas: {len(lista_todas_incidencias)}')
    print(f'Total de incidencias válidas: {len(lista_incidencias_validas)}')
    print(f'Total de incidencias erróneas: {len(lista_incidencias_erroneas)}')
    print(f'Porcentaje de incidencias "Molt Urgent": {porcentaje_molt_urgent:.2f}%')

    # Crear estadísticas de las incidencias
    estadisticas = {
        "total_incidencias": len(lista_todas_incidencias),
        "incidencias_validas": len(lista_incidencias_validas),
        "incidencias_erroneas": len(lista_incidencias_erroneas),
        "incidencias_molt_urgent": incidencias_molt_urgent,
        "porcentaje_molt_urgent": porcentaje_molt_urgent,
        "fecha_procesamiento": str(fecha_actual)
    }

    # Guardar las estadísticas en un archivo JSON
    with open(f'estadisticas_{fecha_actual}.json', 'w', encoding='utf-8') as f:
        json.dump(estadisticas, f, ensure_ascii=False, indent=4)

    # Imprimir las incidencias válidas
    print('Incidencias válidas:')
    for inc in lista_incidencias_validas:
        print(inc)


# Ruta del archivo XML
ruta_archivo_xml = "./Grup 4 - XML Con Excel.xml"

# Llama a la función con la ruta a tu archivo XML
extraer_incidencias(ruta_archivo_xml)