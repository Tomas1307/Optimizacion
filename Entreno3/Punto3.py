#-------
# AUTHORS
# t.acosta - 202011237
# l.guerrerom - 202021248 
#-------

import pulp as lp
import pandas as pd
import matplotlib.pyplot as plt

def optiPets():
    conjuntos = pd.read_excel(io="Punto2.xlsx", sheet_name='Sensibilidad')

    I = [i for i in conjuntos["Insumo"]] 
    T = ["Cachorro","Adulto"]
    #Tiempos procesamiento kg
    tiempo = [2,3]

    #P
    cantidad = pd.read_excel(io="Punto2.xlsx", sheet_name='Sensibilidad',index_col=0).squeeze()
    produccion = pd.read_excel(io="Punto2.xlsx", sheet_name='Produccion',index_col=(0,1)).squeeze()

    print(produccion[("Cachorro","Pollo")])
    

    # Parametros

    #Disponibilidad semanal del ingrediente
    d = {i: cantidad[i] for i in I if not pd.isna(i)}
    print(d)

    #Capacidad maxima produccion
    c = 50

    #Minutos maximos semanales
    h = 6*60

    #Kg necesarios
    k = {(i,j): produccion[(i,j)] for i in T for j in I if not pd.isna(i) and not pd.isna(j)}
    
    #Tiempo en min de procesamiento del tipo de producto 6 horas a minutos

    t = {T[0]:tiempo[0], T[1]:tiempo[1]}

    #Utilidad
    u = {T[0]:7000, T[1]:6000}

    #Creacion Problema

    prob = lp.LpProblem("Punto3",sense= lp.LpMaximize)

    #Variables

    x={j:lp.LpVariable(f'cantidad_producida_para_{j}',lowBound=(0),cat=lp.LpContinuous)for j in T}
    
    #Restricciones


    #No superar horas maximas de produccion

    prob += sum(x[j] * t[j] for j in T) <= h

    #No superar la disponibilidad del tipo de producto

    for i in I:
        prob += sum(x[j] * k[(j,i)] for j in T) <= d[i]

    #No superar la capacidad de produccion

        prob += sum(x[j] for j in T) <= c

    #Funcion Objetivo

        prob += sum(x[j] * u[j] for j in T)

    #Solucionar

    prob.solve()

    results = "Minimizar Costos:\t" + str(prob.objective.value())
    results += "\nValores de las variables:\n"

    for var in prob.variables():
        results += f"{var.name}: {var.value()}\n"

    


print(optiPets())