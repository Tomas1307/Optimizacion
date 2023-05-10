#-------
# AUTHORS
# t.acosta - 202011237
# al.martinezc1 - 202012606
#-------

import pulp as lp
import pandas as pd


def optimizacion(file_name):
    conjuntos = pd.read_excel(io=file_name, sheet_name='Tabla 2.1')
    #print(conjuntos)
    F=[1,2,3,4,5,6,7,8,9,10]
    V=["Camion","Carro","Moto"]

    capacidad = [200,125,75]
    alquiler = [1.2,0.8,0.5]
    gasolina = [0.2,0.12,0.10]
    Distancias = [81,69,87,90,94,67,67,71,73,80]

    #Creacion Conjuntos
    for i in conjuntos['Finca']:
        if not pd.isna(i):
            F.append(i)
            #print(i)
    #print(F)

    

    #Parametros

    #Capacidad de produccion de la finca i en F
    k_i = {i:conjuntos['Capacidad de producción [kg]'][i-1] for i in F}
    #print(k_i)

    #Costo adecuacion de la finca i en F
    c_i = {i:conjuntos['Costo de adecuación [Millones COP]'][i-1] for i in F}
    #print(c_i)
    
    #Distancia de finca i en F
    d_i ={i:Distancias[i-1] for i in F }
    #print(d_i)
    
    #Capacidad vehiculo
    s_j={}
    for j in V:
        if j == "Camion":
            s_j["Camion"] = capacidad[0]
        if j == "Carro":
            s_j["Carro"] = capacidad[1]
        if j == "Moto":
            s_j["Moto"] = capacidad[2]
    #print(s_j)
    #Alquiler
    a_j ={}
    for j in V:
        if j == "Camion":
            a_j["Camion"] = alquiler[0]
        if j == "Carro":
            a_j["Carro"] = alquiler[1]
        if j == "Moto":
            a_j["Moto"] = alquiler[2]

    #Consumo de un vehiculo

    g_j ={}
    for j in V:
        if j == "Camion":
            g_j["Camion"] = gasolina[0]
        if j == "Carro":
            g_j["Carro"] = gasolina[1]
        if j == "Moto":
            g_j["Moto"] = gasolina[2]
    #print(g_j)


    t = {}
    for j in V:
        if j == "Camion":
            t["Camion"] = 1
        if j == "Carro":
            t["Carro"] = 2
        if j == "Moto":
            t["Moto"] = 4

    #Precio gasolina

    e = 2500

    #monto maximo adecuacion fincas

    p = 55000000

    #limite produccion minimo

    l = 4000



    #Creacion del problema

    x =lp.LpVariable.dicts("la finca se usa",[(i)for i in F],0,1,lp.LpBinary)

    y={(j,i):lp.LpVariable(f'vehiculo_{j}_en_finca{i}',lowBound=0,cat=lp.LpInteger)for j in V for i in F}

    modelo = lp.LpProblem('Punto_2', sense = lp.LpMinimize)

    #Restricciones

    #.	Se debe cumplir un límite mínimo de cacao producido desde las fincas.
    modelo += lp.lpSum(y[j,i]*s_j[j] for i in F for j in V)>= l
    #.	No superar el presupuesto
    modelo += lp.lpSum(x[i]*c_i[i] for f in F)<= p
    
    #Las Fincas 2,8 y 10 no cuentan con carreteras de acceso. 
    for i in [2, 8, 10]:
        modelo += (y["Camion", i]) == 0

    for i in F:
        #No se puede transportar mas de lo producido por una fina 
        modelo += lp.lpSum(s_j[j]*y[j,i] for j in V)<=(k_i[i]*x[i])
        for j in V:
            #enviar la cantidad determinada de vehículos a una finca
            modelo += y[j,i] <= (t[j]*x[i])
        
    

    #funcion objetivo
    modelo += lp.lpSum(y[j,i]*(a_j[j])+d_i[i]*e*g_j[j] for j in V for i in F)
    modelo.solve()
    print("Funcion Objetivo:\t",modelo.objective.value(),"\n")

    print('Status: ', lp.LpStatus[modelo.status])
    print()

    #Valor de la función objetivo
    print(round(lp.value(modelo.objective),2))
    print('\n')

    print("Tabla de fincas usadas:")
    print("Fincas\tUsada")
    impresas = []  # lista para almacenar las variables ya impresas

    for i in F:
        for j in V:
            if y[j,i].value() == 1:
                if i not in impresas:  # verifica si la variable ya ha sido impresa
                    print(f"{i}\tX")
                    impresas.append(i)  # agrega la variable a la lista de impresas
            else:
                break

print(optimizacion(file_name='Datos.xlsx'))