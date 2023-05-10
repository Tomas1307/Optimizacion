import pulp as lp
import pandas as pd

#----------------------
# Authors
# Tomas Acosta Bernal
# Sergio Andres Beltran
# Luis Guerrero
# Miguel Angel Ortiz
#----------------------


def implementacion():

   
    pedidos = pd.read_excel(io="DemandaHistorica.xlsx", sheet_name='Pedidos')

    
    #--Conjuntos---

    #print(pedidos)
    #Conjunto de tipos de productos i en P

    P = []
    for i in pedidos["Parte"]:
        if not pd.isna(i):
            if i not in P:
                P.append(i)

    #Conjunto de las maquinas especializadas  j in M
    M = [i for i in range(1,6)]
    #print(M)

    #Conjunto de horas disponibles semanales tanto regulares como extra t en T
    T = []
    for i in range(1,25):
        T.append(120+48)

    print(T)
    #Conjunto Turnos disponibles k en U
    #--Parametros--

    rendimiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 2',index_col=0).squeeze()

    alistamiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 3', index_col=0).squeeze()

    demandas = pd.read_excel(io="DemandaHistorica.xlsx", sheet_name="Demanda",index_col=0).squeeze()

    #Demanda semanal promedio para cada producto i en P

    #print(rendimiento)
    

    d_i = {i: demandas[i] for i in P if not pd.isna(i)}

    #cantidad de tiempo disponible de trabajo disponible entre semana

    s = 120

    #cantidad de tiempo extra disponible en fin de semana

    e = 48

    #tasa de produccion del producto i en P de la maquina j en M

    t_ij = {(i,j) : rendimiento[i][j] for i in P for j in M if not pd.isna(rendimiento[i][j])}
    
    #print(t_ij)

    #tiempo requerido en horas del aislamiento de la maquina j en M

    a_ij = {(i,j) : alistamiento[i][j] for i in P for j in M if not pd.isna(alistamiento[i][j])}


    #factores de rendimiento de produccion de cada producto

    f_i = {i : rendimiento[i]["Rendimiento"] for i in P if not pd.isna(i)}

    #--VariablesDecision

    #print(rendimiento["Amortiguadores"]["Rendimiento"])
    

print(implementacion())