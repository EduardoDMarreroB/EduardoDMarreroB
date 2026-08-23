# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

class catalogo():
    """
    Módulo del sistema encargado de la visualización y gestión del inventario de la máquina.
    Mapea de forma bidimensional (filas y columnas) la disponibilidad de los artículos,
    controlando el estado del stock disponible de cara al usuario.
    """
    def __init__(self, matriz: dict, filas: int, columnas: int):
        self.nombre_modulo: str = "Catálogo"
        self.matriz: dict = matriz
        self.filas: int = filas
        self.columnas: int = columnas

    def ver(self):
        """
        Despliega en consola la interfaz visual de los productos registrados.
        Evalúa de forma dinámica si hay stock o si el artículo se encuentra
        totalmente agotado, mostrando precios formateados y sus respectivas coordenadas.
        """
        print("\n--- CATÁLOGO DE PRODUCTOS ---")
        if not self.matriz:
            print("[MÁQUINA VACÍA]")
            return
        
        for prod in self.matriz.values(): 
            if prod.cantidad_stock > 0:
                print(f"[{prod.coordenada_ajedrez}] - {prod.nombre_completo} | Precio: ${prod.precio:.2f} | Stock: {prod.cantidad_stock}")
            else:
                print(f"[{prod.coordenada_ajedrez}] - {prod.nombre_completo} | Precio: ${prod.precio:.2f} | -- AGOTADO --")

    def update_vista(self):
        """
        Disparador encargado de refrescar y actualizar en tiempo real el catálogo
        mostrado en la terminal tras cada transacción o cambio en el inventario.
        """
        self.ver()