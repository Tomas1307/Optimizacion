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

    #monto maximo adecuacion fincas

    p = 55000000

    #limite produccion minimo

    l = 4000



    #Creacion del problema

    modelo = lp.LpProblem('Punto_2', sense = lp.LpMinimize)

    x =lp.LpVariable.dicts("la finca se usa",[(i)for i in F],0,1,lp.LpBinary)

    y={(i,j):lp.LpVariable(f'finca_{i}_en_vehiculo_{j}',lowBound=0,cat=lp.LpInteger)for i in F for j in V}

    #Restricciones

# a.No es posible enviar más de 1 camión, 2 carros y 4 motos a una finca. 
    for i in F:
        for j in V:
            if i not in [2,8,10]:
                if j == 'Camion':
                    print(i,j)
                    modelo += y[i,j] <= 1
            if j == "Carro":
                modelo += y[i,j] <= 2
            if j == "Moto":
                modelo += y[i,j] <=4
            else:
                modelo += y[i,j] <= 0
# b.No superar el presupuesto
    modelo += lp.lpSum(c_i[i]*x[i] <= p for i in F)

# c.Se debe cumplir un limite minimo de caco producido desde las fincas

    modelo += lp.lpSum(s_j[j]*y[i,j] <= l for i in F for j in V)

# d.No se puede transportar mas de lo producido por una finca
    for i in F:
        modelo += lp.lpSum(s_j[j]*y[i,j] <= k_i[i]*x[i] for j in V)



    


    #Variables de decision

print(optimizacion(file_name='Datos.xlsx'))   