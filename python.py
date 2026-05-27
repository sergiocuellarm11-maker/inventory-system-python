from datetime import datetime
print("🛒Bienvenido al sistema de inventarios💹")
print("-"*40)
inventario = [ ]
def agregar_producto():
    nombre = input("Ingresa el nombre del producto: ").upper()
    
        
    try:
        precio = float(input("Ingresa el precio del producto: "))
        cantidad = int(input("Ingresa la cantidad: "))
        total = precio * cantidad

        diccionario = {
        "nombre" : nombre,
        "precio" : precio,
        "cantidad" : cantidad,
        "total" : total
        }
        inventario.append(diccionario)
        print(f"Producto {nombre} agregado correctamente✅")
    except ValueError:
        print("❌Error: Recuerda que solo van numeros en precio y cantidad")
    print("-"*40)
def mostrar_inventario( ):
    if len(inventario) == 0:
        print("El inventario esta vacio")
    else:
        for i in inventario:
            print(f"Producto : {i['nombre']}")
            print(f"Precio : ${i['precio']:.2f}")
            print(f"Cantidad : {i['cantidad']}")
            print(f"Total : ${i['total']:.2f}")
            print("-"*40)
def eliminar_producto():
    nombre_a_eliminar = input("Ingrese el nombre del producto a eliminar".strip()).upper()
    for i in inventario:
        if nombre_a_eliminar == i['nombre']:
            inventario.remove(i)
            print("Producto eliminado correctamente✅ ")
            return
    print("El producto no existe❌")
def total_inventario():
    gran_total = 0
    for i in inventario:
        gran_total += i["total"]
    print(f"💰 El valor total de todo el inventario es: ${gran_total:.2f}")
def guardar_en_plantilla():
    ahora = datetime.now()
    reporte_fecha= ahora.strftime("%d/%m/%Y %H:%M:%S")
    with open("reporte_inventario.txt", "w", encoding="utf-8") as archivo:
        archivo.write("="*50 +"\n")
        archivo.write(" |        REPORTE DE INVENTARIO PROFESIONAL  |" + "\n")
        archivo.write("="*50 +"\n")
        archivo.write(f"{'PRODUCTO':<20} | {'CANT.':>7} | {'PRECIO':>10} | {'TOTAL':>10}\n")
        gran_total = 0
        for item in inventario:
            linea = (f"{item['nombre'].capitalize():<20} | "
                    f"{item['cantidad']:>7} | "
                    f"${item['precio']:>9} | "
                    f"${item['total']:>9}\n")
            archivo.write(linea)
            gran_total += item["total"]
        
        # 4. Pie de página con el total global
        archivo.write("-" * 50 + "\n")
        archivo.write(f"{'VALOR TOTAL DEL INVENTARIO:':<40} ${gran_total:>8}\n")
        archivo.write("="*50 + "\n")
        archivo.write(f"Reporte generado el: {reporte_fecha}\n")
        archivo.write("="*50 + "\n")
    print("✅ ¡Plantilla organizada guardada en 'reporte_inventario.txt'!")
def Agregar_al_Existente():
    ahora = datetime.now()
    # Solo una marca de tiempo corta para la línea
    fecha_linea = ahora.strftime("%d/%m %H:%M")
    
    with open("reporte_inventario.txt", "a", encoding="utf-8") as archivo:
        # Si la lista está vacía, avisamos
        if not inventario:
            print("⚠️ No hay productos nuevos en la lista para agregar.")
            return
        gran_total_final = 0
        for i in inventario:
            # Añadimos la fecha al inicio de la línea para control
            linea = (f"{fecha_linea} | {i['nombre'].capitalize():<15} | "
                    f"{i['cantidad']:>5} | ${i['total']:>9.2f}\n")
            archivo.write(linea)
        archivo.write("-" * 50 + "\n")
        archivo.write(f"{'TOTAL DE ESTA ENTRADA:':<40} ${gran_total_final:>8.2f}\n")
        archivo.write("="*50 + "\n")    
    print("✅ Items agregados al final del archivo existente.")

def salir():

    print("👋Hasta pronto")
    

while True:
    print("1-Agregar Producto")
    print("2-Eliminar Producto")
    print("3-Mostrar Inventario")
    print("4-Valor Total Inventario")
    print("5-Guardar inventario en Archivo TXT")
    print("6-Agregar archivo al existente TXT")
    print("7-Salir")
    print("-"*40)
    op = input("Ingrese la opcion a realizar")
    if op == "1":
        agregar_producto()
    elif op =="2":
        eliminar_producto()
    elif op =="3":
        mostrar_inventario()
    elif op == "4":
        total_inventario()
    elif op == "5":
        guardar_en_plantilla()
    elif op == "6":
        Agregar_al_Existente()
    elif op =="7":
        salir()
        break
    else:
        print("-"*40)
        print("La opcion no es valida")
    



