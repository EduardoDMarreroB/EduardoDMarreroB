# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

from producto import producto

class restock():
    """
    Módulo administrativo encargado de gestionar el reabastecimiento de la máquina.
    Esta clase permite al operador o administrador de la máquina expendedora 
    restaurar los niveles de inventario de los productos al tope operativo, 
    actualizando tanto las existencias en memoria como las métricas de control.
    """
    def __init__(self):
        self.nombre_modulo: str = "Restock"
        self.opcion: int = 0
        self.cant_agregada: int = 0
        self.new_producto: str = ""

    def cargar(self, diccionario_productos):
        """
        Recorre el inventario de la máquina y restablece el stock de cada producto.
        """
        print("\n--- MÓDULO DE RESTOCK (STOCKER) ---")
        coordenada = input("Ingrese la coordenada del producto a gestionar (ej. A1): ").strip().upper()
        
        if coordenada in diccionario_productos:
            encontrado = diccionario_productos[coordenada]
            print(f"Producto encontrado: {encontrado.nombre_completo} (Stock actual: {encontrado.cantidad_stock})")
            try:
                nueva_cant = int(input("Ingrese la nueva cantidad total en stock: "))
                encontrado.actualizar_stock(nueva_cant)
                print(f"[ÉXITO] Stock actualizado a {nueva_cant} unidades.")
            except ValueError:
                print("[ERROR] Cantidad inválida.")
        else:
            print("[INFO] Coordenada nueva detectada. Creando nuevo producto...")
            codigo = input("Código de 5 letras: ").strip().upper()[:5]
            nombre = input("Nombre completo: ").strip()
            try:
                precio = float(input("Precio: "))
                stock = int(input("Cantidad inicial de stock: "))
                despedida = input("Mensaje de despedida: ").strip()
                
                nuevo = producto(coordenada, codigo, nombre, precio, stock, despedida, stock, 0)
                diccionario_productos[coordenada] = nuevo
                print(f"[ÉXITO] Nuevo producto '{nombre}' añadido en {coordenada}.")
            except ValueError:
                print("[ERROR] Datos numéricos inválidos.")