# 🔍 Analizador de Logs de Autenticación

Herramienta en Python para analizar archivos `.log` del sistema y detectar intentos de autenticación fallidos, con visualización de resultados y exportación a CSV.

---

## 🚀 Funcionalidades

✅ Lectura y análisis línea por línea de archivos `.log`  
✅ Búsqueda de patrones personalizados mediante expresiones regulares  
✅ Detección de IPs involucradas en errores de autenticación  
✅ Visualización en tablas con la librería `tabulate`  
✅ Exportación a un archivo `.csv` con los resultados  

---

## 🛠️ Tecnologías utilizadas

- Python 3.x
- `argparse`
- `re` (expresiones regulares)
- `csv`
- `collections.Counter`
- `tabulate` 📦 (para mostrar tablas bonitas)

---

## 📦 Instalación

Asegúrate de tener `tabulate` instalado:

```bash
sudo apt install python3-tabulate


📄 Uso
python3 lectura.py --log /ruta/del/log.log --patron "authentication failure" [--ver-ips] [--output resultado.csv]


🔧 Parámetros
Parámetro	Descripción
--log	Ruta del archivo .log a analizar (obligatorio)
--patron	Patrón o palabra clave a buscar (expresión regular)
--ver-ips	(Opcional) Muestra las IPs encontradas y su frecuencia
--output	(Opcional) Nombre del archivo CSV de salida. Por defecto: analisis_logs.csv

📈 Ejemplo
python3 lectura.py --log /var/log/auth.log --patron "authentication failure" --ver-ips --output errores.csv


Salida esperada:
📋 Analizador de logs de autenticación

🔍 Se encontraron 10 coincidencias
+---------------------------+-------------+----------+
| Fecha                    | IP          | Usuario  |
+---------------------------+-------------+----------+
| 2025-06-14T23:41:29.63Z   | 127.0.0.1   | dani     |
| ...                      | ...         | ...      |
+---------------------------+-------------+----------+

📊 IPs que aparecen en los errores:
+-------------+--------+
| IP          | Veces  |
+-------------+--------+
| 127.0.0.1   | 5      |
+-------------+--------+

✅ El archivo CSV fue creado correctamente.
📄 Total de líneas exportadas: 10


💼 ¿Por qué este proyecto?
Este script fue desarrollado como práctica para demostrar:

Capacidad para procesar y analizar datos de sistema.

Manejo de expresiones regulares.

Uso de librerías estándar y externas (como tabulate).

Escribir código limpio, modular y bien documentado.

Ideal para desarrolladores o técnicos de seguridad que quieran automatizar el análisis de logs.

🧠 Autor
Daniel -> danigst



