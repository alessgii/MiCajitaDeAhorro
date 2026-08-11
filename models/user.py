class User:
    def __init__ (self, name, password):
        self.name = name
        self.password = password
        self.balance = 0
        self.recent_activity = []

    def deposito(self, monto):
        if monto <= 0: return "El monto de deposito debe ser mayor que $0"
        
        # agregar fecha
        # fecha_transaccion = time.strftime(formato_fecha)
        self.balance += monto
        self.recent_activity.append(f"Deposito de ${monto}")
        return "200"

    def retirar(self, monto):
        if monto > self.balance: return "Saldo insuficiente"
        if monto <= 0: return "El monto de retiro debe ser mayor que $0"

        # agregar fecha
        # fecha_transaccion = time.strftime(formato_fecha)
        self.balance -= monto
        self.recent_activity.append(f"Retiro de ${monto}")
        return "200"
