#Dividedos de coca cola
#compro 2 acciones de coca cola por mes
precio_accion= 69.31  # Precio de la acción de Coca-Cola

dividendo_trimestral_por_accion = 0.51  # Dividendos por acción

# Inicializar variables
periodo = 0  # Contador de períodos

# Ganancias por dividendos
ganancias_por_dividendos = 0  # Variable para registrar las ganancias por dividendos

cantidad_de_acciones_compradas=0 # Variable para registrar la cantidad de acciones compradas

cantidad_de_acciones_generando_ganancias = 0 # Variable para registrar la cantidad de acciones compradas

while ganancias_por_dividendos < 100:
    
    cantidad_de_acciones_compradas += 2  # Se compran dos acciones cada vez

    resto = periodo % 3  # Resto de la división entre 3 para determinar el trimestre

    cantidad_de_trimestres = (periodo - resto) /3

    if cantidad_de_trimestres > 0 :
        cantidad_de_acciones_generando_ganancias += 2
    else: 
        cantidad_de_acciones_generando_ganancias = 0
    
    periodo += 1
    ganancias_por_dividendos = cantidad_de_acciones_generando_ganancias * dividendo_trimestral_por_accion  # Calcular las ganancias por dividendos

print(f'Cantidad de períodos necesarios: {periodo} meses')
print(f'Ganancias por dividendos: {ganancias_por_dividendos:.2f}')
print(f'Cantidad de acciones compradas: {cantidad_de_acciones_compradas:.2f}')
print(f'Cantidad de acciones generando ganancias: {cantidad_de_acciones_generando_ganancias:.2f}')
print(f'Cantidad invertida: {precio_accion * cantidad_de_acciones_compradas:.2f}')