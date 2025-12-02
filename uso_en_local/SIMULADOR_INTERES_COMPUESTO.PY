ahorro = 100000  # Cantidad de pesos invertidos por mes
interes = 0.08  # Interés en broker bitcoins
cantidad_de_periodos = 0
pozo_acumulado = 0
ganancias_por_intereses = 0  # Variable para registrar las ganancias por intereses

while ganancias_por_intereses < ahorro:  # Condición basada en las ganancias por intereses
    tasa_anual = 0.08  # Tasa nominal anual
    tasa_mensual = (1 + tasa_anual)**(1/12) - 1  # Tasa mensual efectiva
    intereses_generados = pozo_acumulado * tasa_mensual  # Intereses generados en el período
    pozo_acumulado += ahorro + intereses_generados  # Actualizar el pozo acumulado
    ganancias_por_intereses += intereses_generados  # Acumular las ganancias por intereses
    cantidad_de_periodos += 1  # Incrementar el contador de períodos

total_anios = int(cantidad_de_periodos / 12)  # Convertir a años
total_meses = cantidad_de_periodos % 12  # Obtener los meses restantes

print(f'Cantidad de períodos necesarios: {cantidad_de_periodos} meses')
print(f'Pozo acumulado final: {pozo_acumulado:.2f}')
print(f'Ganancias por intereses: {ganancias_por_intereses:.2f}')
print(f'Cantidad de años necesarios: {total_anios:.2f} y {total_meses:.2f} meses')