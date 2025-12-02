import openpyxl

ARS_USS = 1354.10 #Valor del dolar en pesos argentinos

periodo = 0 #Año inicial de inversion

INV_ARS = 300000 #Inversión mensual en pesos argentinos
INV_USS = INV_ARS / ARS_USS #Inversión mensual en dólares

cash= 0 #Dinero disponible en caja para invertir

ganancia_anual = 0 #Ganancia anual en pesos argentinos

INV_TOTAL = 0 #Inversión total en pesos argentinos

ganancia_anual_requerida = 12000

TNA=0.1 #Tasa nominal anual de retorno esperada del 8%
TNM= TNA / 12 #Tasa nominal mensual de retorno esperada del 8%

ganancias_totales=0 #Ganancias totales en dolares


while (cash * TNM) < 1000:
    for i in range(1,13):
        INV_TOTAL += INV_ARS

        cash = INV_USS + cash * (1 + TNM) # Reinvertir el dinero en caja del mes anterior

        print(f"Mes {i} del año {periodo}: Inversión mensual: U$S {INV_USS:.2f}; Dinero en caja: U$D {cash:.2f}")
        
        if i==12:
            periodo += 1
            print(" ")

print("Fin del ciclo de inversión con FCI.")
#print(diccionario_dividendos_con_cedears)