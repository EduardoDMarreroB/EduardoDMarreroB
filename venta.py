# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

class venta():
    """
    Módulo operativo encargado de procesar y validar las transacciones comerciales.
    Esta clase actúa como intermediario entre el cliente (tarjeta) y el inventario (producto),
    asegurando que se cumplan las condiciones de saldo y existencias antes de despachar 
    un artículo de la máquina.
    """
    def __init__(self, tarjeta):
        self.nombre_modulo: str = "Venta"
        self.tarjeta = tarjeta

    def cobrar(self, objeto_producto):
        """
        Ejecuta el ciclo de cobro y despacho de un producto.

        Este método verifica que el producto tenga existencias disponibles y que la 
        tarjeta asociada cuente con fondos suficientes. Si ambas condiciones se cumplen, 
        descuenta el saldo, actualiza las estadísticas de venta del producto, reduce 
        su stock en una unidad e imprime el mensaje de despedida en consola.
        """
        if objeto_producto.cantidad_stock <= 0:
            print(f"\n[VENTA RECHAZADA] El producto {objeto_producto.nombre_completo} está agotado.")
            return False
        
        precio = objeto_producto.precio
        
        if self.tarjeta.verificar_saldo(precio):
            self.tarjeta.descontar_saldo(precio)
            objeto_producto.dispensar()
            print(f"[VENTA EXITOSA] Cobrado: ${precio:.2f}. Saldo restante: ${self.tarjeta.saldo:.2f}")
            return True
        else:
            print(f"\n[VENTA RECHAZADA] Saldo insuficiente. Precio: ${precio:.2f} | Tu Saldo: ${self.tarjeta.saldo:.2f}")
            return False