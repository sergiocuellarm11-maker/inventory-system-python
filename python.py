import sqlite3
from datetime import datetime
import csv
import json
def inicializar_db():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS productos (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nombre TEXT UNIQUE NOT NULL,

            precio REAL NOT NULL,

            cantidad INTEGER NOT NULL,

            total REAL NOT NULL

        )

    """)
    
    conexion.commit()
    conexion.close()
print("🛒 Bienvenido al sistema de inventarios con SQL 💹")
print("-" * 40)
inicializar_db()
def agregar_producto():
    nombre = input("Ingresa el nombre del producto: ").upper()
    
    while True:
        try:
            precio = float(input("Ingresa el precio del producto: "))
            if precio < 0:
                print("ERROR: El precio no puede ser negativo")
            else:
                break
        except ValueError:
            print("Recuerda que solo se aceptan números")

    while True:
        try:
            cantidad = int(input("Ingresa la cantidad: "))
            if cantidad < 0:
                print("ERROR: No puede haber cantidad negativa")
            else:
                break
        except ValueError:
            print("Recuerda que solo van números positivos")

    total = precio * cantidad

    # GUARDAR EN SQL
    try:
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, cantidad, total) VALUES (?, ?, ?, ?)",(nombre, precio, cantidad, total))
        conexion.commit()
        print(f"Producto {nombre} agregado correctamente a la DB ✅")
    except sqlite3.IntegrityError:
        print(f"❌ Error: El producto '{nombre}' ya existe en el inventario.")
    finally:
        conexion.close()
    print("-" * 40)
def mostrar_inventario():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio, cantidad, total FROM productos")
    filas = cursor.fetchall()
    
    if not filas:
        print("El inventario está vacío.")
    else:
        print("\n--- LISTA DE PRODUCTOS ---")
        for i in filas:
            print(f"Producto : {i[0]}")
            print(f"Precio   : ${i[1]:.2f}")
            print(f"Cantidad : {i[2]}")
            print(f"Total    : ${i[3]:.2f}")
            print("-" * 40)
    conexion.close()
def eliminar_producto():
    nombre_a_eliminar = input("Ingrese el nombre del producto a eliminar: ").strip().upper()
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE nombre = ?", (nombre_a_eliminar,))
    
    if cursor.rowcount > 0:
        print("Producto eliminado correctamente ✅")
    else:
        print("El producto no existe ❌")
    
    conexion.commit()
    conexion.close()
def total_inventario():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT SUM(total) FROM productos")
    resultado = cursor.fetchone()[0]
    gran_total = resultado if resultado else 0
    print(f"💰 El valor total de todo el inventario es: ${gran_total:.2f}")
    conexion.close()
def buscar_producto():
    nombre_busqueda = input("Ingrese el nombre del producto: ").upper()
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre_busqueda,))
    producto = cursor.fetchone()
    
    if producto:
        print(f"PRODUCTO : {producto[1]}")
        print(f"CANTIDAD : {producto[3]}")
        print(f"PRECIO   : {producto[2]}")
        print(f"TOTAL    : {producto[4]}")
    else:
        print(f"El producto {nombre_busqueda} no existe")
    conexion.close()
def guardar_en_plantilla():
    ahora = datetime.now()
    reporte_fecha = ahora.strftime("%d/%m/%Y %H:%M:%S")
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, precio, cantidad, total FROM productos")
    items = cursor.fetchall()

    with open("reporte_inventario.txt", "w", encoding="utf-8") as archivo:
        archivo.write("="*50 +"\n")
        archivo.write(" |         REPORTE DE INVENTARIO PROFESIONAL  |" + "\n")
        archivo.write("="*50 +"\n")
        archivo.write(f"{'PRODUCTO':<20} | {'CANT.':>7} | {'PRECIO':>10} | {'TOTAL':>10}\n")
        gran_total = 0
        for item in items:
            linea = (f"{item[0].capitalize():<20} | {item[2]:>7} | ${item[1]:>9.2f} | ${item[3]:>9.2f}\n")
            archivo.write(linea)
            gran_total += item[3]
        
        archivo.write("-" * 50 + "\n")
        archivo.write(f"{'VALOR TOTAL DEL INVENTARIO:':<40} ${gran_total:>8.2f}\n")
        archivo.write("="*50 + "\n")
        archivo.write(f"Reporte generado el: {reporte_fecha}\n")
    conexion.close()
    print("✅ ¡Plantilla TXT guardada!")
def guardar_csv():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, cantidad, precio, total FROM productos")
    datos = cursor.fetchall()
    
    with open("Reporte_Generado.csv", "w", newline="", encoding="utf-8") as archivo:
        escribir = csv.writer(archivo)
        escribir.writerow(["PRODUCTO", "CANT.", "PRECIO", "TOTAL"])
        for fila in datos:
            escribir.writerow(fila)
    conexion.close()
    print("✅ ¡Reporte CSV creado!")
def guardar_json():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre, cantidad, precio, total FROM productos")
    filas = cursor.fetchall()
    
    inventario_lista = []
    for f in filas:
        inventario_lista.append({"PRODUCTO": f[0], "CANTIDAD": f[1], "PRECIO": f[2], "TOTAL": f[3]})
    
    reporte = {"Fecha": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Inventario": inventario_lista}
    
    with open("Reporte_Generado.json", "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=4, ensure_ascii=False)
    conexion.close()
    print("✅ Archivo JSON creado!")
def actualizar_stock():
    nombre_producto_actualizar =  input("Ingresa el nombre del producto").upper()    
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT precio FROM productos WHERE nombre =?", (nombre_producto_actualizar,))
    resultado = cursor.fetchone()
    if resultado:
        try:
            while True:
                try:
                    precio_nuevo = float(input("Ingresa el nuevo precio del producto"))
                    if precio_nuevo< 0:
                        print("ERROR: El precio no puede ser en negativo")
                    else:
                        break
                except ValueError:
                    print("Recuerda que solo se aceptan numeros")
            while True:
                try:
                    nueva_cantidad = int(input("Ingresa la nueva cantidad del producto"))
                    if nueva_cantidad < 0:
                        print("ERROR: Recuerda que no deben ir cantidades negativas")
                    else:
                        break
                except ValueError:
                    print("Recuerda que solo se aceptan numeros")
            nuevo_total = nueva_cantidad * precio_nuevo
            cursor.execute("""
                UPDATE productos
                SET cantidad= ?, precio =?, total =?
                WHERE nombre= ?
                """,(nueva_cantidad,precio_nuevo,nuevo_total,nombre_producto_actualizar))
            conexion.commit()
            print(f"✅ Producto '{nombre_producto_actualizar}' actualizado correctamente.")
        except ValueError:
            print("ERROR: Cantidad o Precio deben se numeros")
    
    else:
        print(f"El producto {nombre_producto_actualizar} no existe en la base de datos")
    conexion.close()

while True:
    print("\nMENÚ DE OPCIONES:")
    print("1-Agregar Producto")
    print("2-Eliminar Producto")
    print("3-Mostrar Inventario")
    print("4-Valor Total Inventario")
    print("5-Buscar producto")
    print("6-Actualizar Stock")
    print("7-Guardar en TXT")
    print("8-Guardar en CSV")
    print("9-Guardar en JSON")
    print("10-Salir")
    
    print("-" * 40)
    op = input("Ingrese la opcion a realizar: ")
    
    if op == "1":
        agregar_producto()
    elif op == "2":
        eliminar_producto()
    elif op == "3":
        mostrar_inventario()
    elif op == "4":
        total_inventario()
    elif op == "5":
        buscar_producto()
    elif op == "6":
        actualizar_stock()
    elif op == "7":
        guardar_en_plantilla()
    elif op == "8":
        guardar_csv()
    elif op == "9":
        guardar_json()
    elif op == "10":
        print("👋 Hasta pronto")
        break
    else:
        print("La opcion no es valida")



