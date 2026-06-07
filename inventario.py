import io
import json
import csv
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, Response

# 1. Configuración Inicial del Servidor (Boilerplate obligatorio)
app = Flask(__name__)
app.secret_key = 'mi_clave_secreta_para_alertas_y_seguridad'

# Constante global para centralizar el nombre de la base de datos
DATABASE = "inventario.db"

# 2. Inicialización de la Base de Datos SQLite
def inicializar_db():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            total REAL NOT NULL
        )
    """)
    conexion.commit()
    conexion.close()

# Ejecutamos la función para asegurar que el archivo 'inventario.db' exista al arrancar
inicializar_db()

# 3. RUTA PRINCIPAL: Muestra la interfaz web y la tabla con los datos
@app.route('/')
def index():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    
    # Extraemos todos los productos ordenados por ID de forma ascendente
    cursor.execute("SELECT * FROM productos ORDER BY id ASC")
    productos = cursor.fetchall()
    
    # Calculamos la sumatoria total de todo el dinero invertido
    cursor.execute("SELECT SUM(total) FROM productos")
    resultado_total = cursor.fetchone()[0]
    gran_total = resultado_total if resultado_total is not None else 0.0
    
    conexion.close()
    
    # Enviamos el HTML inyectándole las variables calculadas en Python
    return render_template('inventario.html', productos=productos, gran_total=gran_total)

# 4. RUTA DE ACCIÓN: Recibe datos del formulario e inserta un nuevo registro (Método POST)
@app.route('/agregar', methods=['POST'])
def agregar_producto():
    # Extraemos los datos del paquete seguro 'request.form' usando el atributo 'name' del HTML
    nombre = request.form.get('nombre').strip().upper()
    precio = float(request.form.get('precio'))
    cantidad = int(request.form.get('cantidad'))
    total = precio * cantidad  # Lógica matemática en el servidor

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    try:
        cursor.execute("INSERT INTO productos (nombre, precio, cantidad, total) VALUES (?, ?, ?, ?)",
                       (nombre, precio, cantidad, total))
        conexion.commit()
        flash(f"✅ ¡Producto '{nombre}' agregado exitosamente al inventario!", "success")
    except sqlite3.IntegrityError:
        # Si el nombre ya existe en la columna UNIQUE, atrapamos el error para que la app no colapse
        flash(f"❌ Error: El producto '{nombre}' ya se encuentra registrado.", "danger")
    finally:
        conexion.close() # Garantizamos el cierre seguro de la conexión
        
    return redirect(url_for('index'))

# 5. RUTA DE ACCIÓN: Actualiza el stock o precio buscando por nombre (Método POST)
@app.route('/actualizar', methods=['POST'])
def actualizar_producto():
    nombre = request.form.get('nombre').strip().upper()
    nuevo_precio = float(request.form.get('precio'))
    nueva_cantidad = int(request.form.get('cantidad'))
    nuevo_total = nuevo_precio * nueva_cantidad

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    
    # Primero verificamos si el producto realmente existe en la base de datos
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
    if cursor.fetchone() is None:
        flash(f"⚠️ Error: El producto '{nombre}' no existe en el inventario actual.", "danger")
    else:
        # Si existe, actualizamos sus campos y recalculamos su total unitario
        cursor.execute("UPDATE productos SET precio = ?, cantidad = ?, total = ? WHERE nombre = ?",
                       (nuevo_precio, nueva_cantidad, nuevo_total, nombre))
        conexion.commit()
        flash(f"🔄 ¡Producto '{nombre}' actualizado correctamente!", "success")
        
    conexion.close()
    return redirect(url_for('index'))

# 6. RUTA DINÁMICA DE ACCIÓN: Elimina un registro usando su ID único que viaja en la URL (Método GET implícito)
@app.route('/eliminar/<int:id>')
def eliminar_producto(id):
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()
    
    flash("❌ Producto eliminado permanentemente del sistema.", "success")
    return redirect(url_for('index'))

# 7. RUTAS DE REPORTES: Generan archivos al vuelo directamente desde la memoria RAM
@app.route('/reporte/txt')
def reporte_txt():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    output = io.StringIO()
    output.write("=======================================================\n")
    output.write("                REPORTE DE INVENTARIO WEB              \n")
    output.write("=======================================================\n")
    output.write(f"{'ID':<6}{'PRODUCTO':<22}{'PRECIO':<10}{'CANTIDAD':<10}{'TOTAL':<10}\n")
    output.write("-" * 55 + "\n")
    for prod in productos:
        output.write(f"{prod[0]:<6}{prod[1]:<22}${prod[2]:-9.2f}   {prod[3]:<7}${prod[4]:-9.2f}\n")

    res = Response(output.getvalue(), mimetype="text/plain")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_inventario.txt"
    return res

@app.route('/reporte/csv')
def reporte_csv():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Producto', 'Precio', 'Cantidad', 'Total'])
    for prod in productos:
        writer.writerow([prod[0], prod[1], prod[2], prod[3], prod[4]])

    res = Response(output.getvalue(), mimetype="text/csv")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_inventario.csv"
    return res

@app.route('/reporte/json')
def reporte_json():
    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()

    lista_productos = []
    for prod in productos:
        lista_productos.append({
            "id": prod[0],
            "producto": prod[1],
            "precio": prod[2],
            "cantidad": prod[3],
            "total": prod[4]
        })

    json_data = json.dumps(lista_productos, indent=4, ensure_ascii=False)
    res = Response(json_data, mimetype="application/json")
    res.headers["Content-Disposition"] = "attachment; filename=reporte_inventario.json"
    return res

# Interruptor de encendido del servidor con Debug activo
if __name__ == '__main__':
    app.run(debug=True)