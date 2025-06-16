import __main__
import mimetypes
import re
from collections import Counter

#Este programa abrira y leera los log, para poder clasificarlos, ver si hay inicios de sesion sospechosos


#Usamos esta funcion para abrir el archivo log
def abrir_archivo(archivo_log):
    try:
        print(f"Intentando abir {archivo_log}")
        with open(archivo_log, "r") as f:
            for line in f:
                yield line.strip()

    except Exception as e :
        print(f"error archivo no encontrado {e}")


#Verificar que el archivo es un tipo .log
def comprobar_tipo_archivo(nombre_archivo):
    #tipo,_ = mimetypes.guess_type(nombre_archivo)
    #if tipo == "text/plain":
     #   return True
    #return False
    return nombre_archivo.endswith(".log")

#Funcion que usaremos para buscar coincidencias, sospechosas en el log
def busqueda_incidencias(elemento_coincidencia, ruta_log):
    patron = fr"{elemento_coincidencia}"
    coincidencias = []

    for linea in abrir_archivo(ruta_log):
        coincidencia = re.search(patron, linea)
        if coincidencia:
            coincidencias.append(linea)
    return coincidencias


#Funcion para comparar la busqueda y contarla
def contador_busqueda(coincidencias, palabra_buscar):
    contador = Counter()

    for linea in coincidencias:
        #PRimero hay que hacer el search(), despues el .group(), porque si no falla
        match = re.search(palabra_buscar, linea)
        if match:
            palabra = match.group()
            contador[palabra] += 1
    return contador

def main():
    #obtenemos el archivo
    ruta_nombre = input("Introduzca la ubicacion del archivo, junto al nombre (ejemplo: /var/log/auth.log)").strip()
    
    #comprobamos que es un tipo log
    while(True):
        if(comprobar_tipo_archivo(ruta_nombre)):
            print(f"Se abrio correctamente el archivo{ruta_nombre}")
            break
        else:
            print("Debe introducir un archivo .log correcto")
            ruta_nombre = input("Introduzca la ubicacion del archivo, junto al nombre (ejemplo: /var/log/auth.log)")
    #abrir_archivo(ruta_nombre)

    patron = input("busquemos una coincidencia, introduce un patron: (por ejemplo: authentication failure):")
    resultados = busqueda_incidencias(patron, ruta_nombre)

    if resultados:
        print(f"Se encontraron un numero de  {len(resultados)} coincidencias")
        for i in resultados:
            print("-",i)
    else: 
        print("ningun resultado encontrado")

if __name__ == "__main__":
    main()