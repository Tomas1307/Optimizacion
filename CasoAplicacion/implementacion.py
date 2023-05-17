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

    #cantidad de tiempo disponible de trabajo entre semana

    h = 120

    #cantidad de tiempo extra disponible en fin de semana

    e = 48

    #factores de rendimiento de produccion de cada producto

    f_i = {i : rendimiento[i]["Rendimiento"] for i in P if not pd.isna(i)}

    #print(f_i)

    #print(rendimiento)
    

    d_i = {i: demandas[i] for i in P if not pd.isna(i)}


    #print(d_i)

    #tiempo requerido en horas del aislamiento de la maquina j en M

    a_ij = {(i,j) : alistamiento[i][j] for i in P for j in M if not pd.isna(alistamiento[i][j])}


    #tasa de produccion de la parte i en P de la maquina j en M

    t_ij = {(i,j) : rendimiento[i][j] for i in P for j in M if not pd.isna(rendimiento[i][j])}
    
    #costo de horas extra maquina
    
    c = 30

    #costo horas extra personal de apoyo

    q = 40

    #Creacion problema

    prob = lp.LpProblem('CasoAplicacion', sense = lp.LpMinimize)

    
    #--VariablesDecision

    #Variable binaria si se escoge la maquina para producir la parte
    x={(i,j):lp.LpVariable(f'Si_se_escoge_maquina_{j}_para_parte_{i}',lowBound=0,cat=lp.LpBinary)for i in P for j in M }

    y={(i,j):lp.LpVariable(f'si_se_alista_maquina_{j}_para_parte_{i}',lowBound=0,cat=lp.LpBinary)for i in P for j in M }

    R={(i,j):lp.LpVariable(f'Horas_regulares_maquina_{j}_para_parte_{i}',lowBound=0,cat=lp.LpContinuous)for i in P for j in M }

    O={(i,j):lp.LpVariable(f'Horas_extra_maquina_{j}_para_parte_{i}',lowBound=0,cat=lp.LpContinuous)for i in P for j in M }


    
    #Restricciones
    for i in P:
        #No tener inventario/satisfacer la demanda semanal:
        prob += sum((O[i,j] + R[i,j])* t_ij[(i,j)]for j in M if (i,j) in t_ij) * f_i[i] == d_i[i] 
        #No superar la cantidad de horas regulares
        prob += sum(R[i,j] for j in M) <= h 
        #No superar la cantidad de horas extras
        prob += sum(O[i,j] for j in M) <= e 

        for j in M:

            #Si se decide alistar la maquina se debe producir mínimo una unidad del producto 
            prob += x[i,j] + y[i,j] != 1

            #Para producir la parte se debe alistar la maquina

            prob += y[i,j] >= x[i,j]

            #Solo se debe alistar una vez la maquina 

            prob += y[i,j] <= 1

    for j in M:

        #Debe cumplirse el tiempo de alistamiento 
        prob += sum(R[i,j] >= a_ij[i,j] * y[i,j] for i in P if (i,j) in a_ij) 

    #print(rendimiento["Amortiguadores"]["Rendimiento"])

    #Funcion Objetivo

    prob += sum(O[i,j]*(c+q) for i in P for j in M)

    #Resolver problema

    prob.solve()

    #Imprimir resultados
    print("Minimizar costos extra:\t",prob.objective.value(),"\n")

    #Imprimir variables
    for variable in prob.variables():
        if "Horas_extra" in variable.name and variable.varValue > 0:
            print(variable.varValue)
        
    

    

print(implementacion())