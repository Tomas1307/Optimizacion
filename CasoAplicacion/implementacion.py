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

    #Conjunto de horas disponibles semanales tanto regulares como extra t en T
    T = []
    for i in range(1,25):
        T.append(i)

    #print(T)
    #Conjunto Turnos disponibles k en U
    #--Parametros--

    rendimiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 2',index_col=0).squeeze()

    alistamiento = pd.read_excel(io="data.xlsx", sheet_name='Tabla 3', index_col=0).squeeze()

    demandas = pd.read_excel(io="data.xlsx", sheet_name="Demanda",index_col=0).squeeze()

    #Demanda semanal promedio para cada producto i en P

    #print(rendimiento)
    

    d_i = {i: demandas[i] for i in P if not pd.isna(i)}


    #print(d_i)

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

    #print(f_i)


    #--VariablesDecision

    y={(i,j,t):lp.LpVariable(f'producto_{i}_en_maquina{j}',lowBound=0,cat=lp.LpBinary)for i in P for j in M for t in T}

    x={(i,j,t):lp.LpVariable(f'uso_de_maquina_{j}_para_producto{i}_a_la_hora_{t}',lowBound=0,cat=lp.LpBinary)for i in P for j in M for t in T}

    z={(i,j,t):lp.LpVariable(f'maquina_{j}_alistando_para_producto_{i}_a_la_hora_{t}',lowBound=0,cat=lp.LpBinary)for i in P for j in M for t in T}

   

    #Creacion problema

    prob = lp.LpProblem('Punto_2', sense = lp.LpMinimize)

    #Restricciones


    for t in T:

        #No exceder horas de trabajo semanales disponibles
        prob += sum(((x[i,j,t] * f_i[i])/t_ij[i,j]) + sum(y[i,j,t] * a_ij[i,j]) for i in P for j in M if (i,j) in a_ij) <= e+s

        #Alistamiuento solo se realiza una vez por producto por maquina
        prob += sum(y[i,j,t] for i in P for j in M) <= 1

        #Garantizar que se cumpla el tiempo de alistamiento

        prob += sum(y[i,j,t] == a_ij[i,j] for i in P for j in M if (i,j) in a_ij)

        #Una maquina solo se puede usar para producir una cosa en un momento especifico
        #MUCHOS PEROS
        prob += sum(x[i,j,t] for j in M for t in T) <= 1

        for j in M:
            #cumplir con demanda
            prob += sum(x[i,j,t] * f_i[i] == d_i[i] for i in P) 

            for i in P:
                #Una maquina no se puede alistar sin que se pueda terminar su tiempo de alistamiento
                if (i, j) in a_ij:
                    if t + a_ij[i,j] - 1 > len(T) and j in a_ij:
                        prob += y[i,j,t] == 0

         

    #print(rendimiento["Amortiguadores"]["Rendimiento"])
    

print(implementacion())