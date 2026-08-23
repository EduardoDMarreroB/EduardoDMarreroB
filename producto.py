# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

class producto():
    """
    Representa un artículo disponible dentro del inventario de la máquina expendedora.
    Esta clase gestiona la información comercial del producto, su ubicación en el 
    sistema de coordenadas, el control de existencias (stock) y el historial de 
    unidades dispensadas para la auditoría de ventas.
    """
    def __init__(self, coordenada_ajedrez: str, codigo_cinco_letras: str, nombre_completo: str, precio: float, cantidad_stock: int, mensaje_despedida: str, cantidad_ultimo_stock: int, cantidad_vendida: int):
        self.coordenada_ajedrez = coordenada_ajedrez
        self.codigo_cinco_letras = codigo_cinco_letras
        self.nombre_completo = nombre_completo
        self.precio = precio
        self.cantidad_stock = cantidad_stock
        self.mensaje_despedida = mensaje_despedida
        self.cantidad_ultimo_stock = cantidad_ultimo_stock
        self.cantidad_vendida = cantidad_vendida

    def dispensar(self):
        """
        Ejecuta el proceso físico y lógico de despacho del artículo.
        Verifica la disponibilidad de inventario, decrementa el stock actual,
        actualiza el contador de unidades vendidas y emite los mensajes de
        confirmación pertinentes en la interfaz de usuario.
        """
        if self.cantidad_stock > 0:
            self.cantidad_stock -= 1
            self.cantidad_vendida += 1
            print(f"\n[MÁQUINA] Dispensando: {self.nombre_completo}")
            print(f"[MÁQUINA] {self.mensaje_despedida}")
            return True
        else:
            print(f"\n[ERROR] Lo sentimos, {self.nombre_completo} está agotado.")
            return False

    def actualizar_stock(self, nueva_cantidad: int):
        """
        Modifica y sincroniza los niveles de existencias del producto en la máquina.
        Asigna el nuevo volumen de inventario disponible y redefine el registro
        del último stock cargado para los módulos de auditoría y reportes.
        """
        self.cantidad_stock = nueva_cantidad
        self.cantidad_ultimo_stock = nueva_cantidad