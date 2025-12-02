inversion_mensual=200
caja=0
TNA=0.12
TNA_mensual=TNA/12
TNA_diaria=(1+TNA_mensual)**(1/30)-1
dias_totales=0
contador_dias=0
contador_años=0
contador_meses=0
while caja<24000:
    if dias_totales%30==0:
        caja=caja*TNA_diaria+inversion_mensual
    else:
        caja=caja*TNA_diaria
    dias_totales+=1
    contador_años= dias_totales//365
    contador_meses= (dias_totales-contador_años*365)//30
    contador_dias=dias_totales-contador_años*365-contador_meses*30

print(f'Se tardo: {contador_años:.2f} años, {contador_meses:.2f} meses y  {contador_dias} días para alcanzar los 24000 USD')