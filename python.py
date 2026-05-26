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
        
def salir():
    print("👋Hasta pronto")
while True:
    print("1-Agregar Producto")
    print("2-Eliminar Producto")
    print("3-Mostrar Inventario")
    print("4-Valor Total Inventario")
    print("5-Salir")
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
    elif op =="5":
        salir()
        break
    else:
        print("-"*40)
        print("La opcion no es valida")
    



