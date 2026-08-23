import json
import os
import requests

from producto import producto
from tarjeta import tarjeta   
from catalogo import catalogo
from venta import venta
from restock import restock
from reporte import reporte


class maquina_expendedora():
    """
    Clase principal que controla el flujo operativo de la máquina expendedora,
    gestionando la sincronización de datos con GitHub, la persistencia local,
    la interfaz de usuario por consola y el procesamiento de compras.
    """

    def __init__(
        self,
        archivo_inventario: str,
        archivo_clientes: str,
        url_productos_github: str,
        url_clientes_github: str,
        archivo_reporte: str,
        ruta_graficos: str
    ):
        self.archivo_inventario = archivo_inventario
        self.archivo_clientes = archivo_clientes
        self.url_productos_github = url_productos_github
        self.url_clientes_github = url_clientes_github
        self.archivo_reporte = archivo_reporte
        self.ruta_graficos = ruta_graficos

        self.diccionario_productos = {}
        self.lista_tarjetas = []

        # Archivo local con los números de tarjeta de demostración
        # y su correspondiente ID de cliente.
        self.archivo_tarjetas = os.path.join(
            os.path.dirname(__file__),
            "data",
            "tarjetas_demo.json"
        )

        # Relación entre número de tarjeta de demostración e ID de cliente.
        self.tarjetas_demo = {}

    def cargar_tarjetas_demo(self):
        """
        Carga la relación entre los números de tarjeta de demostración
        y los identificadores de cliente desde un archivo JSON local.
        """
        try:
            with open(self.archivo_tarjetas, "r", encoding="utf-8") as f:
                tarjetas = json.load(f)

            self.tarjetas_demo = {
                str(t["numero"]): str(t["id_cliente"])
                for t in tarjetas
            }

            print("Tarjetas de demostración cargadas correctamente.")

        except FileNotFoundError:
            print("[ERROR] No se encontró tarjetas_demo.json.")
            self.tarjetas_demo = {}

        except (json.JSONDecodeError, KeyError, TypeError):
            print("[ERROR] El archivo tarjetas_demo.json no tiene un formato válido.")
            self.tarjetas_demo = {}

    def guardar_datos_locales(self):
        """
        Sincroniza y escribe el estado actual del inventario de productos
        y el saldo de los clientes en archivos locales JSON al cerrar
        el programa.
        """
        try:
            # 1. Guardar productos localmente
            productos_dict = []

            for p in self.diccionario_productos.values():
                productos_dict.append({
                    "cod": p.coordenada_ajedrez,
                    "prod": p.nombre_completo,
                    "precio": p.precio,
                    "despedida": p.mensaje_despedida,
                    "cantidad_stock": p.cantidad_stock,
                    "cantidad_ultimo_stock": p.cantidad_ultimo_stock,
                    "cantidad_vendida": p.cantidad_vendida
                })

            with open(
                self.archivo_inventario,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    productos_dict,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

            # 2. Guardar clientes/tarjetas localmente
            clientes_dict = []

            for t in self.lista_tarjetas:
                clientes_dict.append({
                    "id": int(t.hash_numero),
                    "saldo": t.saldo
                })

            with open(
                self.archivo_clientes,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    clientes_dict,
                    f,
                    indent=2,
                    ensure_ascii=False
                )

        except Exception as e:
            print(f"[ERROR] No se pudieron guardar los archivos locales: {e}")

    def iniciar(self):
        """
        Arranca la máquina expendedora intentando descargar los datos
        actualizados desde GitHub. Si falla la conexión, carga los
        respaldos locales de seguridad.
        """

        print("--- Iniciando Máquina Expendedora ---")

        cabeceras = {
            "User-Agent": "Python-VendingMachine"
        }

        # ==========================================
        # 1. CARGAR PRODUCTOS
        # ==========================================

        print("Descargando inventario desde GitHub...")

        try:
            res_prod = requests.get(
                self.url_productos_github,
                headers=cabeceras,
                timeout=3
            )

            if res_prod.status_code == 200:

                for p in res_prod.json():

                    nuevo_prod = producto(
                        p["cod"],
                        p["cod"],
                        p["prod"],
                        float(p["precio"]),
                        10,
                        p["despedida"],
                        10,
                        0
                    )

                    self.diccionario_productos[
                        nuevo_prod.coordenada_ajedrez.upper()
                    ] = nuevo_prod

                print("¡Inventario cargado con éxito desde GitHub!")

            else:
                raise FileNotFoundError

        except Exception:

            try:
                with open(
                    self.archivo_inventario,
                    "r",
                    encoding="utf-8"
                ) as f:

                    for p in json.load(f):

                        nuevo_prod = producto(
                            p["cod"],
                            p["cod"],
                            p["prod"],
                            float(p["precio"]),
                            int(p.get("cantidad_stock", 10)),
                            p["despedida"],
                            int(p.get("cantidad_ultimo_stock", 10)),
                            int(p.get("cantidad_vendida", 0))
                        )

                        self.diccionario_productos[
                            nuevo_prod.coordenada_ajedrez.upper()
                        ] = nuevo_prod

                print("Inventario local cargado exitosamente.")

            except FileNotFoundError:
                print(
                    "Archivo local de inventario no encontrado. "
                    "Máquina VACÍA."
                )

        # ==========================================
        # 2. CARGAR CLIENTES
        # ==========================================

        print("Descargando lista de clientes desde GitHub...")

        try:
            res_clientes = requests.get(
                self.url_clientes_github,
                headers=cabeceras,
                timeout=3
            )

            if res_clientes.status_code == 200:

                for c in res_clientes.json():

                    nueva_tarjeta = tarjeta(
                        str(c["id"]),
                        float(c["saldo"]),
                        0.0
                    )

                    self.lista_tarjetas.append(nueva_tarjeta)

                print(
                    "¡Clientes y saldos cargados con éxito desde GitHub!"
                )

            else:
                raise FileNotFoundError

        except Exception:

            try:
                with open(
                    self.archivo_clientes,
                    "r",
                    encoding="utf-8"
                ) as f:

                    for c in json.load(f):

                        nueva_tarjeta = tarjeta(
                            str(c["id"]),
                            c["saldo"],
                            0.0
                        )

                        self.lista_tarjetas.append(nueva_tarjeta)

                print("Clientes locales cargados exitosamente.")

            except FileNotFoundError:
                print("No se encontró el archivo local de clientes.")

        # ==========================================
        # 3. CARGAR TARJETAS DE DEMOSTRACIÓN
        # ==========================================

        self.cargar_tarjetas_demo()

        # ==========================================
        # 4. INICIAR MENÚ
        # ==========================================

        self.menu_principal()

    def menu_principal(self):
        """
        Ciclo principal de la interfaz por consola. Captura las entradas
        del usuario para procesar inserción de tarjetas, compras, logout
        y comandos administrativos.
        """

        tarjeta_activa = None

        while True:

            print("\n==============================")

            if tarjeta_activa:
                print(
                    f"[SESIÓN ACTIVA] Tarjeta: "
                    f"{tarjeta_activa.hash_numero} | "
                    f"Saldo: ${tarjeta_activa.saldo:.2f}"
                )
            else:
                print("[SESIÓN] No hay ninguna tarjeta ingresada.")

            mi_catalogo = catalogo(
                self.diccionario_productos,
                3,
                3
            )

            mi_catalogo.ver()

            entrada = input(
                "\nIntroduzca Código (ej. CocaC), Tarjeta, "
                "comando (RS/RP) o SALIR: "
            ).strip()

            entrada_upper = entrada.upper()

            # ==========================================
            # SALIR
            # ==========================================

            if entrada_upper == "SALIR":

                self.guardar_datos_locales()

                print(
                    "Datos guardados localmente. "
                    "Apagando máquina..."
                )

                break

            # ==========================================
            # RESTOCK
            # ==========================================

            elif entrada_upper == "RS":

                modulo_rs = restock()

                modulo_rs.cargar(
                    self.diccionario_productos
                )

                self.guardar_datos_locales()

                continue

            # ==========================================
            # REPORTE
            # ==========================================

            elif entrada_upper == "RP":

                modulo_rp = reporte(
                    self.archivo_reporte,
                    self.ruta_graficos
                )

                modulo_rp.creartxt(
                    self.diccionario_productos,
                    self.lista_tarjetas
                )

                modulo_rp.graph(
                    self.diccionario_productos
                )

                continue

            # ==========================================
            # LOGOUT
            # ==========================================

            elif entrada_upper == "LOGOUT":

                tarjeta_activa = None

                print("Tarjeta retirada.")

                continue

            # ==========================================
            # BÚSQUEDA DEL PRODUCTO
            # ==========================================

            if entrada_upper in self.diccionario_productos:

                producto_seleccionado = (
                    self.diccionario_productos[entrada_upper]
                )

                if tarjeta_activa is None:

                    print(
                        "\n[MÁQUINA] Por favor, "
                        "pase primero su tarjeta antes "
                        "de seleccionar un producto."
                    )

                else:

                    proceso_venta = venta(
                        tarjeta_activa
                    )

                    if proceso_venta.cobrar(
                        producto_seleccionado
                    ):

                        self.guardar_datos_locales()

                continue

            # ==========================================
            # VERIFICACIÓN DE TARJETA
            # ==========================================

            tarjeta_encontrada = None

            # El usuario introduce el número corto de la tarjeta.
            # Se busca su ID correspondiente en tarjetas_demo.json.
            id_cliente = self.tarjetas_demo.get(
                entrada
            )

            if id_cliente:

                for t in self.lista_tarjetas:

                    if t.hash_numero == id_cliente:

                        tarjeta_encontrada = t
                        break

            if tarjeta_encontrada:

                tarjeta_activa = tarjeta_encontrada

                print(
                    "\n[MÁQUINA] ¡Tarjeta aceptada! "
                    "Sesión iniciada."
                )

            else:

                print(
                    "\n[ERROR] Entrada no reconocida "
                    "(No es un producto válido o tarjeta registrada)."
                )


if __name__ == "__main__":

    # URLs de los archivos JSON publicados en el repositorio.
    # Estas URLs se actualizarán después de subir los archivos
    # al repositorio de GitHub.

    url_prod = (
        "https://raw.githubusercontent.com/"
        "EduardoDMarreroB/maquina-expendedora-python/"
        "main/data/productos.json"
    )

    url_clie = (
        "https://raw.githubusercontent.com/"
        "EduardoDMarreroB/maquina-expendedora-python/"
        "main/data/clientes.json"
    )

    maquina = maquina_expendedora(
        archivo_inventario="inventario.json",
        archivo_clientes="clientes.json",
        url_productos_github=url_prod,
        url_clientes_github=url_clie,
        archivo_reporte="reporte_ventas.txt",
        ruta_graficos="graficos_data"
    )

    maquina.iniciar()