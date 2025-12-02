def vinodradov(diccionario_capa):
    NP=diccionario_capa["NP"]
    divisores = []
    for i in range(1, NP + 1):
        if NP % i == 0:
            divisores.append(i)
    #print(f"Divisores comunes={divisores}")
    numeros_excluidos = [i for i in range(1, NP + 1) if i not in divisores]
    #print(f"numeros_excluidos{numeros_excluidos}")
    PTR=[]
    a=[]
    b=[]
    Dcco=[]
    #Agregamos los valores por defeto, para el caso del paso unitario
    PTR.append(1)
    a.append(1)
    b.append(NP-1)
    Dcco.append(1/(2*1))

    for numeros_excluido in numeros_excluidos:
    
        A=[]
        B=[]
        C=[]
        D=[]
        E=[]
        A.append(NP)  # Agrega NP como el primer elemento
        A.append(numeros_excluido)  # Agrega numeros_excluido como el segundo elemento
        B.append(0)
        B.append(0)
        C.append(1)
        C.append(0)
        D.append(0)
        D.append(1)
        E.append(0)
        E.append(1)

        contador=2
        while A[contador-1]>0:
            A.append(A[contador-2]%A[contador-1]) #calculamos el modulo o residuo y lo guardamos en el vector A
            contador=contador+1
        A.append(0)
        if A[contador-2]==1:
            for j in range(2,contador):
                B.append(int(A[j-2]/A[j-1]))
                C.append(B[j]*C[j-1]+C[j-2])
                D.append(B[j]*D[j-1]+D[j-2])
                E.append(-E[j-1])
            
            if D[contador - 2] not in b:
                if A[1]>(NP/2):
                    dcco=1/(2*(A[1]-NP))
                    PTR.append(A[1]-NP)
                    Dcco.append(dcco)
                else:
                    dcco=1/(2*(A[1]))
                    PTR.append(A[1])
                    Dcco.append(dcco)
                a.append(C[contador-2])
                b.append(D[contador-2])
                
    #print(f"NP={NP}, PTR={PTR}, a={a}, b={b}")
    patrones_posibles=[]
    for ptr, val_a, val_b, dcco in zip(PTR, a, b, Dcco):
        patrones_posibles.append([NP, ptr, val_a, val_b, dcco])
    # Ordena patrones_posibles por el valor de val_b (4° elemento en cada sublista)
    patrones_posibles.sort(key=lambda x: x[1])
    #print(f"patrones_posibles{patrones_posibles}")
    diccionario_capa["patrones_posibles"] = patrones_posibles
    return patrones_posibles

def obteniendo_orden_del_patron(NP, paso):
    variable=1
    patron=[]
    while len(patron)<NP:
        patron.append(variable)
        variable=variable+paso
        if variable>NP:
            variable=variable-NP
    #print(patron)
    return patron