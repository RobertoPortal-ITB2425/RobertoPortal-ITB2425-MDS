import xml.etree.ElementTree as ET
from datetime import datetime
import json
import os


def validar_fecha(fecha_str):
    """Valida que la fecha esté en formato DD/MM/YYYY."""
    try:
        datetime.strptime(fecha_str, "%d/%m/%Y")
        return True
    except ValueError:
        print("Error: La fecha no tiene el formato DD/MM/YYYY.")
        return False


def extraer_incidencias(xml_file, json_file):
    try:
        # Verificar si el archivo XML existe
        if not os.path.exists(xml_file):
            print("Error: Archivo XML no encontrado.")
            return

        # Cargar y parsear el archivo XML
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError:
            print("Error: El archivo XML no está bien formado.")
            return

        # Inicializar listas y contadores
        lista_todas_incidencias = []
        lista_incidencias_validas = []
        contador_tipo_incidencias = {"Hardware": 0, "Software": 0}
        contador_detalles_incidencias = {}
        contador_niveles_urgencia = {}

        # Obtener la fecha actual
        fecha_actual = datetime.today().date()
        inicio_periodo = datetime(fecha_actual.year, 9, 1).date()
        fin_periodo = datetime(fecha_actual.year, 12, 31).date()

        # Iterar sobre cada incidencia en el XML
        for incidencia in root.findall('.//Incidencia'):
            try:
                incidencia_data = {
                    "codigo_estudiante": incidencia.find('Codigo_de_estudiante').text,
                    "aula": incidencia.find('Aula').text,
                    "fecha": incidencia.find('Fecha_en_la_que_ocurrió_por_primera_vez').text,
                    "tipo_incidencia": incidencia.find('Tipo_de_incidencia').text,
                    "detalle_incidencia": incidencia.find('Detalle_de_la_incidencia').text,
                    "nivel_urgencia": incidencia.find('Nivel_de_urgencia').text,
                }
            except AttributeError:
                print("Error: Faltan algunos datos en la incidencia.")
                continue

            lista_todas_incidencias.append(incidencia_data)

            # Validar las condiciones
            try:
                codigo_valido = len(incidencia_data["codigo_estudiante"]) == 9
                aula_valida = 100 <= int(incidencia_data["aula"]) <= 399
                fecha_valida = validar_fecha(incidencia_data["fecha"]) and inicio_periodo <= datetime.strptime(
                    incidencia_data["fecha"], "%d/%m/%Y").date() <= fin_periodo
            except (ValueError, TypeError):
                print("Error: Datos de incidencia no válidos.")
                continue

            if codigo_valido and aula_valida and fecha_valida:
                lista_incidencias_validas.append(incidencia_data)

                # Contar tipos de incidencias
                contador_tipo_incidencias[incidencia_data["tipo_incidencia"]] += 1

                # Contar detalles de incidencias
                detalle = incidencia_data["detalle_incidencia"]
                contador_detalles_incidencias[detalle] = contador_detalles_incidencias.get(detalle, 0) + 1

                # Contar niveles de urgencia
                nivel = incidencia_data["nivel_urgencia"]
                contador_niveles_urgencia[nivel] = contador_niveles_urgencia.get(nivel, 0) + 1

        # Calcular porcentajes
        total_incidencias_validas = len(lista_incidencias_validas)
        porcentajes_tipo = {tipo: round((count / total_incidencias_validas) * 100, 2) for tipo, count in
                            contador_tipo_incidencias.items() if total_incidencias_validas > 0}
        porcentajes_detalles = {detalle: round((count / total_incidencias_validas) * 100, 2) for detalle, count in
                                contador_detalles_incidencias.items() if total_incidencias_validas > 0}
        porcentajes_niveles = {nivel: round((count / total_incidencias_validas) * 100, 2) for nivel, count in
                               contador_niveles_urgencia.items() if total_incidencias_validas > 0}

        # Preparar los resultados para exportar
        resultados = {
            "fecha_de_creación": datetime.now().isoformat(),
            "total_incidencias_encontradas": len(lista_todas_incidencias),
            "total_incidencias_validas": total_incidencias_validas,
            "porcentajes_tipo_incidencias": porcentajes_tipo,
            "porcentajes_detalles_incidencias": porcentajes_detalles,
            "porcentajes_niveles_urgencia": porcentajes_niveles
        }

        # Guardar resultados en un archivo JSON
        try:
            with open(json_file, 'a', encoding='utf-8') as f:
                json.dump(resultados, f, ensure_ascii=False, indent=4)
                f.write('\n')
        except IOError:
            print("Error: No se pudo escribir en el archivo JSON.")

        # Imprimir resultados en la consola
        print(f'Total de incidencias encontradas: {len(lista_todas_incidencias)}')
        print(f'Total de incidencias válidas: {total_incidencias_validas}')

        print('Porcentajes de tipos de incidencias:')
        for tipo, porcentaje in porcentajes_tipo.items():
            print(f'{tipo}: {porcentaje:.2f}%')

        print('Porcentajes de detalles de incidencias:')
        for detalle, porcentaje in porcentajes_detalles.items():
            print(f'{detalle}: {porcentaje:.2f}%')

        print('Porcentajes de niveles de urgencia:')
        for nivel, porcentaje in porcentajes_niveles.items():
            print(f'{nivel}: {porcentaje:.2f}%')

    except Exception as e:
        print(f"Error inesperado: {e}")


# Ruta del archivo XML
ruta_archivo_xml = 'TA03.xml'
# Ruta del archivo JSON de salida
ruta_archivo_json = 'Resultados.json'

# Llama a la función con la ruta a tu archivo XML y la ruta del archivo JSON
extraer_incidencias(ruta_archivo_xml, ruta_archivo_json)
