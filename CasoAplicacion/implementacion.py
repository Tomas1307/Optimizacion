import pulp as lp
import pandas as pd
import matplotlib.pyplot as plt

#----------------------
# Authors
# Tomas Acosta Bernal
# Sergio Andres Beltran
# Luis Guerrero
# Miguel Angel Ortiz
#----------------------


def implementacion():

    
    partes = pd.read_excel(io="data.xlsx", sheet_name='Demanda')

    #print(partes) 
    
    #--Conjuntos---

    #print(pedidos)
    #Conjunto de tipos de productos i en P
    
    P = []
    for i in partes["Partes"]:
        if not pd.isna(i):
            if i not in P:
                P.append(i)
    
    #print(P)

    #Conjunto de las maquinas especializadas  j in M
    M = [i for i in range(1,6)]
    #print(M)

    #--Parametros--

    rendimiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 2',index_col=0).squeeze()

    alistamiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 3', index_col=0).squeeze()

    demandas = pd.read_excel(io="data.xlsx", sheet_name="Demanda",index_col=0).squeeze()

    #Demanda semanal promedio para cada producto i en P

    #cantidad de tiempo regular de trabajo

    h = 120

    #cantidad de tiempo extra disponible en fin de semana

    e = 48

    #factores de rendimiento de produccion de cada parte

    f = {i : rendimiento[i]["Rendimiento"] for i in P if not pd.isna(i)}

    print("f[i]",f["Amortiguadores"])

    #print(rendimiento)
    
    #Demanda semanal de la parte i en P
    d = {i: demandas[i] for i in P if not pd.isna(i)}




    print(d)

    #tiempo requerido en horas del aislamiento de la maquina j en M

    a = {(i,j) : alistamiento[i][j] for i in P for j in M if not pd.isna(alistamiento[i][j])}

    #print(a["Amortiguadores",1])
    #tasa de produccion de la parte i en P de la maquina j en M

    t = {(i,j) : rendimiento[i][j] for i in P for j in M if not pd.isna(rendimiento[i][j])}

    prob = lp.LpProblem('CasoAplicacion', sense = lp.LpMinimize)

    
    #--VariablesDecision

    #Variable binaria si se escoge la maquina para producir la parte
    X = {(i, j): lp.LpVariable(f'Si_se_escoge_maquina_{j}_para_producir_{i}', cat=lp.LpBinary) for i in P for j in M}

    R={(i,j):lp.LpVariable(f'Horas_regulares_maquina_{j}_para_{i}',lowBound=0,cat=lp.LpContinuous)for i in P for j in M }

    O={(i,j):lp.LpVariable(f'Horas_extra_maquina_{j}_para_{i}',lowBound=0,cat=lp.LpContinuous)for i in P for j in M }


    
    #Restricciones
    for i in P:
        #No tener inventario/satisfacer la demanda semanal:
        prob += sum((O[i,j] + R[i,j])* t[i,j] * f[i] for j in M if (i,j) in t)  == d[i]

        print (sum((O[i,j] + R[i,j])* t[i,j] * f[i] for j in M if (i,j) in t)  == d[i])
    

    for j in M:

        #No superar la cantidad de horas disponibles

        prob += sum(O[i,j] + R[i,j] + a[i,j] for i in P if (i,j) in a) <= (e + h) 

        #No superar el t en horas extra
        prob += sum(R[i,j] for i in P) <= h - sum(a[i,j]*X[i,j] for i in P if (i,j) in a)

        #No superar el t en horas extra
        prob += sum(O[i,j] <= e *X[i,j] for i in P)

        #print(sum(O[i,j] + R[i,j] + (X[i,j]) * a[i,j] for i in P if (i,j) in a) <= e + h)


    #print(rendimiento["Amortiguadores"]["Rendimiento"])

    #Funcion Objetivo

    prob += sum(O[i,j] for i in P for j in M)

    #Resolver problema

    prob.solve()

    #Imprimir resultados
    print("Minimizar horas extra:\t",prob.objective.value(),"\n")


    #Imprimir variables
    for variable in prob.variables():

        print(variable.name, variable.value())

    
    

    

print(implementacion())