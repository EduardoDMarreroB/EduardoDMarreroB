# Marrero Eduardo y Trujillo Adrián. Algoritmos y Programación Sección 3 2526-3

class tarjeta():
    """
    Representa una unidad de pago electrónica cifrada para interactuar con la máquina.
    Esta clase gestiona la autenticación del identificador de usuario, el control 
    de fondos disponibles (saldo) y el registro histórico del capital debitado.
    """
    def __init__(self, hash_numero, saldo, dinero_gastado):
        self.hash_numero: str = str(hash_numero)
        self.saldo: float = float(saldo)
        self.dinero_gastado: float = float(dinero_gastado)

    def verificar_saldo(self, monto: float):
        """
        Evalúa la viabilidad financiera de una transacción solicitada.
        Compara los fondos actuales en el balance de la tarjeta contra el coste 
        especificado del artículo para validar si la operación es aprobable.
        """
        return self.saldo >= monto

    def descontar_saldo(self, monto: float):
        """
        Ejecuta el débito económico tras una compra exitosa.
        Previa verificación de fondos, substrae el coste del balance disponible,
        acumula el valor en el registro de gastos y confirma la transacción.
        """
        if self.verificar_saldo(monto):
            self.saldo -= monto
            self.dinero_gastado += monto
            return True
        return False