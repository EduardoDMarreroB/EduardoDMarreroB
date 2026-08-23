# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

import os
import matplotlib.pyplot as plt

class reporte():
    """
    Módulo administrativo encargado de compilar el cierre de caja de la máquina,
    generando auditorías en texto plano y analítica visual de rendimiento.
    """
    def __init__(self, archivo_reporte: str, graficos: str):
        self.nombre_modulo: str = "Reporte"
        self.archivo_reporte = archivo_reporte
        self.graficos = graficos  # Esta es la ruta de la carpeta donde se guardará la imagen

    def creartxt(self, diccionario_productos, lista_tarjetas):
        """
        Calcula las métricas de recaudación total, productos dispensados y
        genera un archivo físico estructurado con el desglose del inventario.
        """
        try:
            total_recaudado = sum(t.dinero_gastado for t in lista_tarjetas)
            total_productos_vendidos = sum(p.cantidad_vendida for p in diccionario_productos.values())
            
            with open(self.archivo_reporte, 'w', encoding='utf-8') as f:
                f.write("=========================================\n")
                f.write("         REPORTE DE VENTAS Y BALANCE     \n")
                f.write("=========================================\n\n")
                f.write(f"Total Recaudado por Tarjetas: ${total_recaudado:.2f}\n")
                f.write(f"Total de Productos Dispensados: {total_productos_vendidos} unidades\n\n")
                f.write("--- DESGLOSE POR PRODUCTO ---\n")
                
                for p in diccionario_productos.values():
                    f.write(f"[{p.coordenada_ajedrez}] {p.nombre_completo:<20} | Vendidos: {p.cantidad_vendida:<3} | Stock Restante: {p.cantidad_stock}\n")
            
            print(f"[ÉXITO] Reporte escrito correctamente en '{self.archivo_reporte}'.")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo generar el reporte escrito: {e}")
            return False

    def graph(self, diccionario_productos):
        """
        Genera un gráfico de barras profesional con las unidades vendidas
        utilizando matplotlib y lo guarda automáticamente como una imagen.
        """
        print("\n--- GENERANDO GRÁFICO DE UNIDADES VENDIDAS (MATPLOTLIB) ---")
        
        if not diccionario_productos:
            print("[INFO] No hay datos de productos para graficar.")
            return

        # Extraemos los datos reales del diccionario de productos
        nombres_productos = []
        unidades_vendidas = []
        
        for p in diccionario_productos.values():
            # Incluimos los productos que tienen al menos 1 venta para que el gráfico sea relevante
            if p.cantidad_vendida > 0:
                nombres_productos.append(p.coordenada_ajedrez)
                unidades_vendidas.append(p.cantidad_vendida)
        
        # Si nadie ha comprado nada aún, avisamos y salimos para evitar un gráfico vacío
        if not unidades_vendidas:
            print("[INFO] No hay ventas registradas todavía. No se generará archivo de imagen.")
            return

        try:
            # Aseguramos que la carpeta de destino exista para evitar errores al guardar
            if not os.path.exists(self.graficos):
                os.makedirs(self.graficos)

            # Construimos el gráfico siguiendo la estructura recomendada por el preparador
            plt.figure(figsize=(10, 6)) # Tamaño de la ventana del gráfico
            
            # Creamos gráfico de barras verticales
            plt.bar(nombres_productos, unidades_vendidas, color='skyblue', edgecolor='black')
            
            # Definir etiquetas y títulos
            plt.xlabel('Productos (Códigos)')
            plt.ylabel('Unidades Vendidas')
            plt.title('Reporte Estadístico - Unidades Dispensadas por Producto')
            
            # Añadimos cuadrícula para mejorar la legibilidad del eje Y
            plt.grid(True, axis='y', linestyle='--', alpha=0.7)

            # Guardamos la imagen de forma silenciosa en la carpeta asignada
            ruta_final_imagen = os.path.join(self.graficos, "ventas_productos.png")
            plt.savefig(ruta_final_imagen, bbox_inches='tight')
            plt.close() # Limpiar la memoria de matplotlib
            
            print(f"[ÉXITO] ¡Gráfico estadístico guardado en: {ruta_final_imagen}!")
            
        except Exception as e:
            print(f"[ERROR] Ocurrió un problema al generar la imagen con matplotlib: {e}")