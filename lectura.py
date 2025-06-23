import __main__
import mimetypes
import re
from collections import Counter
import argparse
import csv
from tabulate import tabulate

# Este programa abre y analiza logs para identificar intentos sospechosos de autenticación.


def abrir_archivo(archivo_log):
    """
    Abre un archivo en modo lectura línea por línea.

    Args:
        archivo_log (str): Ruta del archivo que queremos analizar.

    Yields:
        str: Línea limpia (sin saltos de línea) del archivo.
    """
    try:
        print(f"Intentando abrir {archivo_log}")
        with open(archivo_log, "r") as f:
            for line in f:
                yield line.strip()
    except Exception as e:
        print(f"❌ Error al abrir el archivo: {e}")


def comprobar_tipo_archivo(nombre_archivo):
    """
    Verifica si el archivo proporcionado tiene extensión .log.

    Args:
        nombre_archivo (str): Nombre o ruta del archivo.

    Returns:
        bool: True si es un archivo .log, False en caso contrario.
    """
    return nombre_archivo.endswith(".log")


def busqueda_incidencias(elemento_coincidencia, ruta_log):
    """
    Busca coincidencias en el archivo log según un patrón.

    Args:
        elemento_coincidencia (str): Patrón regex a buscar.
        ruta_log (str): Ruta al archivo log.

    Returns:
        list: Lista de líneas que coinciden con el patrón.
    """
    patron = fr"{elemento_coincidencia}"
    coincidencias = []

    for linea in abrir_archivo(ruta_log):
        if re.search(patron, linea):
            coincidencias.append(linea)
    return coincidencias


def contador_busqueda(coincidencias, palabra_buscar):
    """
    Cuenta cuántas veces aparece una palabra o patrón en las líneas encontradas.

    Args:
        coincidencias (list): Lista de líneas del log con coincidencias previas.
        palabra_buscar (str): Expresión regular a contar.

    Returns:
        Counter: Diccionario con la frecuencia de cada coincidencia.
    """
    contador = Counter()
    for linea in coincidencias:
        match = re.search(palabra_buscar, linea)
        if match:
            palabra = match.group()
            contador[palabra] += 1
    return contador


def recibir_parametros():
    """
    Recoge los parámetros pasados por consola usando argparse.

    Returns:
        argparse.Namespace: Objeto con los argumentos: log, patron, ver-ips y output.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", required=True, help="Ruta del archivo log")
    parser.add_argument("--patron", required=True, help="Patrón a buscar en el log")
    parser.add_argument("--ver-ips", action="store_true", help="Mostrar IPs encontradas")
    parser.add_argument("--output", required=False, default="analisis_logs.csv",
                        help="Exportar resultados a CSV (ej: --output resultados.csv)")
    return parser.parse_args()


def preparar_datos(lista_log_fallidos):
    """
    Extrae y estructura los datos relevantes de cada línea del log.

    Args:
        lista_log_fallidos (list): Lista de líneas del log con errores.

    Returns:
        list: Lista de diccionarios con claves: fecha, usuario, ip y mensaje completo.
    """
    datos_procesados = []

    for linea in lista_log_fallidos:
        fecha_match = re.match(r"^\S+", linea)
        fecha = fecha_match.group() if fecha_match else ""
        ip_match = re.search(r"\d{1,3}(?:\.\d{1,3}){3}", linea)
        ip = ip_match.group() if ip_match else ""
        usuario_match = re.search(r"user=([a-zA-Z0-9]+)", linea)
        usuario = usuario_match.group(1) if usuario_match else ""

        datos_procesados.append({
            "fecha": fecha,
            "usuario": usuario,
            "ip": ip,
            "mensaje completo": linea
        })

    return datos_procesados


def crear_csv(datos, nombre_archivo="analisis_log.csv"):
    """
    Crea un archivo CSV con los datos procesados del log.

    Args:
        datos (list): Lista de diccionarios con los datos del log.
        nombre_archivo (str): Nombre del archivo CSV a crear.
    """
    cabecera = ["fecha", "usuario", "ip", "mensaje completo"]
    with open(nombre_archivo, 'w', newline='') as csvfile:
        escritura = csv.DictWriter(csvfile, fieldnames=cabecera)
        escritura.writeheader()
        for linea in datos:
            escritura.writerow(linea)


def main():
    """
    Función principal del programa:
    - Recoge argumentos.
    - Busca incidencias en el log.
    - Muestra resultados por consola en formato tabla.
    - Exporta a CSV si se indica.
    """
    print("📋 Analizador de logs de autenticación\n")

    args = recibir_parametros()
    ruta_nombre = args.log
    patron = args.patron
    nombre_documento = args.output

    if not comprobar_tipo_archivo(ruta_nombre):
        print("⚠️ El archivo no parece ser un .log")
        return

    resultados = busqueda_incidencias(patron, ruta_nombre)
    datos_preparados = preparar_datos(resultados)

    if resultados:
        print(f"🔍 Se encontraron {len(resultados)} coincidencias")
        tabla_coincidencias = [[d["fecha"], d["ip"], d["usuario"]] for d in datos_preparados]
        print(tabulate(tabla_coincidencias, headers=["Fecha", "IP", "Usuario"], tablefmt="grid"))

        if args.ver_ips:
            ip_pattern = r"\d{1,3}(?:\.\d{1,3}){3}"
            cuenta_ips = contador_busqueda(resultados, ip_pattern)

            print("\n📊 IPs que aparecen en los errores:")
            tabla_ips = [[ip, veces] for ip, veces in cuenta_ips.items()]
            print(tabulate(tabla_ips, headers=["IP", "Veces"], tablefmt="grid"))

        if nombre_documento:
            crear_csv(datos_preparados, nombre_documento)
            print("\n✅ El archivo CSV fue creado correctamente.")
            print(f"📄 Total de líneas exportadas: {len(datos_preparados)}")

    else:
        print("❌ Ningún resultado encontrado")


if __name__ == "__main__":
    main()
