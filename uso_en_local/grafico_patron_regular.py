import matplotlib.pyplot as plt

def grafico_patron_regular(PI, radio, NP, PASO_HELICE, orden_de_patrones, vector_X_cara_a, PASO_EN_Y, CANTIDAD_VUELTAS_HELICE):
    
    # Calcular puntos en X para las caras A y B
    XA = vector_X_cara_a
    XA.append(2*PI*radio)  # Agregar el último punto en XA

    YA = [i * PASO_EN_Y for i in range(NP + 1)]  # Generar valores YA
    YA.append(PASO_HELICE)  # Agregar el último punto en XA

    # Generar áreas para graficar
    AREAS_IDA_1 = []
    AREAS_IDA_2 = []
    AREAS_VUELTA_1 = []
    AREAS_VUELTA_2 = []
    # Graficar áreas
    fig, ax = plt.subplots()
    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Gráfico de secuencia de  Áreas')
    for secuencia in orden_de_patrones:
        NP=len(orden_de_patrones)
        print(secuencia)
        print(NP)
        secuencia=secuencia-1
        print(secuencia)
        # Área entre XA e YB
        for i in range(CANTIDAD_VUELTAS_HELICE):
            print(f"i={i}")
            print(f"YA[0]+PASO_HELICE*i={YA[0]+PASO_HELICE*i}")
            print(f"YA[NP-secuencia-1]+PASO_HELICE*i={YA[NP-secuencia-1]+PASO_HELICE*i}")
            if secuencia!=NP:
                area_ida_1 = [
                    (XA[secuencia], YA[0]+PASO_HELICE*i),
                    (XA[secuencia + 1], YA[0]+PASO_HELICE*i),
                    (XA[NP], YA[NP-secuencia-1]+PASO_HELICE*i),
                    (XA[NP], YA[NP-secuencia]+PASO_HELICE*i)
                ]
            else:
                area_ida_1 = [
                    (XA[secuencia-1], YA[0]+PASO_HELICE*i),
                    (XA[secuencia], YA[0])+PASO_HELICE*i,
                    (XA[NP],YA[NP-secuencia-1]+PASO_HELICE*i)
                ]
            AREAS_IDA_1.append(area_ida_1)
            xs, ys = zip(*area_ida_1)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul

            # Área entre XA e YB
            if secuencia==0:
                area_ida_2 = [
                    (XA[0], YA[NP]+PASO_HELICE*i),
                    (XA[secuencia+1], YA[NP]+PASO_HELICE*i),
                    (XA[0], YA[NP-secuencia-1]+PASO_HELICE*i)
                ]
            else:
                area_ida_2 = [
                    (XA[0], YA[NP-secuencia]+PASO_HELICE*i),
                    (XA[secuencia], YA[NP]+PASO_HELICE*i),
                    (XA[secuencia+1], YA[NP]+PASO_HELICE*i),
                    (XA[0], YA[NP-secuencia-1]+PASO_HELICE*i)
                ]
            AREAS_IDA_2.append(area_ida_2)
            xs, ys = zip(*area_ida_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'b', edgecolor='black')  # Rellenar área ida con azul

        for j in range(CANTIDAD_VUELTAS_HELICE):
            print(f"j={j}")
            if secuencia==NP:
                area_vuelta_1 = [
                    (XA[NP], YA[NP]+PASO_HELICE*j),
                    (XA[NP], YA[NP-1]+PASO_HELICE*j),
                    (XA[NP-1], YA[NP]+PASO_HELICE*j),
                ]
            else:
                area_vuelta_1 = [
                    (XA[secuencia], YA[NP]+PASO_HELICE*j),
                    (XA[secuencia + 1], YA[NP]+PASO_HELICE*j),
                    (XA[NP], YA[secuencia+1]+PASO_HELICE*j),
                    (XA[NP], YA[secuencia]+PASO_HELICE*j)
                ]
            AREAS_VUELTA_1.append(area_vuelta_1)
            xs, ys = zip(*area_vuelta_1)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área vuelta con rojo

            if secuencia==0:
                area_vuelta_2 = [
                    (XA[0], YA[0]+PASO_HELICE*j),
                    (XA[0], YA[1]+PASO_HELICE*j),
                    (XA[1], YA[0]),
                ]
            else:
                area_vuelta_2 = [
                    (XA[secuencia], YA[0]+PASO_HELICE*j),
                    (XA[0], YA[secuencia]+PASO_HELICE*j),
                    (XA[0], YA[secuencia+1]+PASO_HELICE*j),
                    (XA[secuencia+1], YA[0]+PASO_HELICE*j)
                ]
            AREAS_VUELTA_2.append(area_vuelta_2)
            xs, ys = zip(*area_vuelta_2)  # Separar coordenadas X e Y
            ax.fill(xs, ys, 'r', edgecolor='black')  # Rellenar área vuelta con rojo

    print(AREAS_IDA_1)
    print(AREAS_IDA_2)
    print(AREAS_VUELTA_1)
    print(AREAS_VUELTA_2)

    plt.show()

