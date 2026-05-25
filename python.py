print("Bienvenido al sistema de inventarios")
print("-"*40)
inventario = [ ]
def agregar():
    nombre = input("Ingresa el nombre del producto: ")
    precio = float(input("Ingresa el precio del producto: "))
    cantidad = int(input("Ingresa la cantidad: "))
    total = precio * cantidad
    dic = {
    "nombre" : nombre,
    "precio" : precio,
    "cantidad" : cantidad,
    "total" : total
    }
    inventario.append(dic)
    print(f"Producto {nombre} agregado correctamente")
    print("-"*40)
def mostrar( ):
    if len(inventario) == 0:
        print("El inventario esta vacio")
    else:
        for i in inventario:
            print(f"Producto {i['nombre']}")
            print(f"Precio {i['precio']}")
            print(f"Cantidad {i['cantidad']}")
            print(f"Total {i['total']}")
def eliminar():
    nombre_usuario = input("Ingrese el nombre del producto a eliminar".strip())
    for i in inventario:
        if nombre_usuario in i['nombre']:
            inventario.remove(nombre_usuario)
            print("Producto eliminado")
        else:
            if nombre_usuario != i['nombre']:
                print("El producto no existe")
def salir():
    print("Hasta luego")
    

while True:
    print("1-Agregar Producto")
    print("2-Eliminar Producto")
    print("3-Mostrar Inventario")
    print("4-Salir")
    print("-"*40)
    op = input("Ingrese la opcion a realizar")
    if op == "1":
        agregar()
    elif op =="2":
        eliminar()
    elif op =="3":
        mostrar()
    elif op =="4":
        salir()
        break
    else:
        print("-"*40)
        print("La opcion no es valida")
    



