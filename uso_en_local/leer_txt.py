import matplotlib.pyplot as plt

import numpy as np

def leer_txt2(nombre_del_archivo_txt):
    # Inicializar listas para almacenar los valores de X e Y
    X = []
    Y = []
    
    # Abrir el archivo en modo lectura
    try:
        with open(nombre_del_archivo_txt, 'r', encoding='utf-8') as file:
            # Leer el archivo línea por línea
            for linea in file:
                # Buscar las posiciones de 'X' y 'Y'
                inicio_X = linea.find('X ')
                fin_X = linea.find(' Y')
                
                # Buscar las posiciones de 'Y' y 'A'
                inicio_Y = linea.find('Y ')
                fin_Y = linea.find(' A')
                
                # Verificar si ambos caracteres fueron encontrados para X
                if inicio_X != -1 and fin_X != -1:
                    # Extraer el texto entre 'X' y 'Y' y convertirlo a número
                    valor_X = float(linea[inicio_X + 2: fin_X].strip())
                    X.append(valor_X)  # Agregar valor a la lista de X
                
                # Verificar si ambos caracteres fueron encontrados para Y
                if inicio_Y != -1 and fin_Y != -1:
                    # Extraer el texto entre 'Y' y 'A' y convertirlo a número
                    valor_Y = float(linea[inicio_Y + 2: fin_Y].strip())
                    Y.append(valor_Y)  # Agregar valor a la lista de Y
    
    except FileNotFoundError:
        print("No se pudo abrir el archivo")
        return
    
    # Crear el gráfico
    plt.plot(X, Y, 'o-', color='b', markersize=6, linewidth=1.5)
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfico de X contra Y')
    plt.legend(['Datos de X e Y'])
    plt.grid(True)
    plt.show()
    return X, Y

def grafico_polar2(radio, vector):
    # Definir los ángulos (en radianes) y los radios
    theta = np.zeros(len(vector))  # Ángulos de 0 a 2*pi
    for i in range(len(vector)):
        theta[i] = vector[i]
    
    r = radio  # Radio en función del ángulo
    
    # Crear el gráfico polar
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(theta, [r] * len(theta), 'b', linewidth=2)  # 'b' es el color azul
    ax.set_rlim(0, r + 50)
    ax.set_title('Gráfico Polar del orden de bobinado', va='bottom')
    
    # Añadir texto al final del radio
    datos = np.zeros((len(theta), 3))
    for j in range(len(theta)):
        grados = theta[j] * 180 / np.pi
        texto = f"{j + 1} º, [{grados:.2f} º]"
        
        # Añadir el texto en las coordenadas X, Y
        ax.text(theta[j], r, texto, fontsize=10, color='r', rotation=grados)
        datos[j, 0] = j + 1  # Orden
        datos[j, 1] = grados  # Ángulo en grados
        datos[j, 2] = grados % 360  # Ángulo ajustado dentro de 0-360 grados
    
    # Ordenar los datos por la tercera columna y eliminarla
    datos2 = datos[np.argsort(datos[:, 2])]
    datos2 = np.delete(datos2, 2, axis=1)

    # Ajuste de estilos de gráfico
    ax.tick_params(labelsize=12)
    fig.set_size_inches(12, 8)
    
    plt.show()
    
    # Retornar la matriz de datos ordenada
    return datos2

nombre_del_archivo_txt="diam=100_long=360_ang=45.0_ancho=6.5_patron=13.txt"
X, Y = leer_txt2(nombre_del_archivo_txt)

vector_X7 = []
j = []

# Usamos range con un paso de 7 para emular el comportamiento de MATLAB
for i in range(1, len(X), 7):  # En Python, los índices son 0-based, así que empezamos en 1 para tomar el segundo elemento
    vector_X7.append(X[i])
    j.append(i + 1)  # Sumamos 1 para que coincida con el índice 1-based de MATLAB
print(X)
print(vector_X7)
# Llamada a la función grafico_polar2 con el radio y vector generados
datos2 = grafico_polar2(50, vector_X7)