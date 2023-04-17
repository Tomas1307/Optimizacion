import pulp as lp
import pandas as pd


#file_name = 'Datos.xlsx'


# -----------------
# Conjuntos
# -----------------
# Variable de los conjuntos


def optimizacion(file_name):
    conjuntos = pd.read_excel(io=file_name, sheet_name='Tabla 2.1')
    print(conjuntos)
    F=[]
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
    print(d_i)
    
    #Capacidad vehiculo
    s_j={}
    for j in V:
        if j == "Camion":
            s_j["Camion"] = capacidad[0]
        if j == "Carro":
            s_j["Carro"] = capacidad[1]
        if j == "Moto":
            s_j["Moto"] = capacidad[2]
    
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
    print(g_j)


    #Costos

    #c = {i: nc["Costo"][i] for i in P}

    #Creacion del problema

    modelo = lp.LpProblem('Entrenamiento_2', sense = lp.LpMinimize)

    #Variables de decision

print(optimizacion(file_name='Datos.xlsx'))