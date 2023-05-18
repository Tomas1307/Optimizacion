#---------
# Authors
#----------
#Tomas Acosta Bernal
# Luis Guerrero
#---------
import pulp as lp

import matplotlib.pyplot as plp

import pandas as pd


#Literal a
def modeloExplicito():

    #Creacion Conjuntos

    conjuntosRefinerias = pd.read_excel(io="Punto2.xlsx", sheet_name='Capacidad')

    conjuntosPaises = pd.read_excel(io="Punto2.xlsx", sheet_name='Demanda')

    L = [i for i in conjuntosRefinerias["Refineria"]]

    P = [i for i in conjuntosPaises["Pais"]]

    #Parametros

    capacidad = pd.read_excel(io="Punto2.xlsx", sheet_name="Capacidad",index_col=0).squeeze()
    demanda = pd.read_excel(io="Punto2.xlsx", sheet_name='Demanda',index_col=0).squeeze()
    destino = pd.read_excel(io="Punto2.xlsx", sheet_name='Destino', index_col=(0,1)).squeeze()


    #Capacidad de produccion de crudo en litros de la localidad i

    q = {i:capacidad[i] for i in L if not pd.isna(i)} 

    #Demanda en litros de crudo anuales del pais j

    d = {j:demanda[j] for j in P if not pd.isna(j)} 

    #Costo unitario en pesos para enviar crudo desde la localidad i al pais j

    #print(destino["Barrancabermeja","Estados Unidos"])

    c = {(i,j): destino[(i,j)] for i in L for j in P if not pd.isna(i) and not pd.isna(j)}

    #Problema

    modelo = lp.LpProblem(name="literal A",sense=lp.LpMinimize)

    #Variables Decision

    x={(i,j):lp.LpVariable(f'litros_solicitados_localidad_{i}_para_pais_{j}',lowBound=(0),cat=lp.LpContinuous)for i in L for j in P}

    #Para barrancabermeja celebralo curramba

    R1Barranca = x[('Barrancabermeja', 'Estados Unidos')] - c[('Barrancabermeja', 'Estados Unidos')] + x[('Barrancabermeja', 'Japon')] - c[('Barrancabermeja', 'Japon')] + x[('Barrancabermeja', 'Reino Unido')] - c[('Barrancabermeja', 'Reino Unido')]+ x[('Barrancabermeja', 'Canada')] - c[('Barrancabermeja', 'Canada')]

    #Para Cartagena nojoda

    R1Cartagena = x[('Cartagena', 'Estados Unidos')] - c[('Cartagena', 'Estados Unidos')] + x[('Cartagena', 'Japon')] - c[('Cartagena', 'Japon')]+ x[('Cartagena', 'Reino Unido')] - c[('Cartagena', 'Reino Unido')] + x[('Cartagena', 'Canada')] - c[('Cartagena', 'Canada')]

    #Para ortito digo Orito

    R1Orito = x[('Orito', 'Estados Unidos')] - c[('Orito', 'Estados Unidos')]+ x[('Orito', 'Japon')] - c[('Orito', 'Japon')]+ x[('Orito', 'Reino Unido')] - c[('Orito', 'Reino Unido')]+ x[('Orito', 'Canada')] - c[('Orito', 'Canada')]

    modelo += R1Barranca + R1Cartagena + R1Orito

    #Restricciones
    #-----------------------------------------------------
    #No superar la capacidad de produccion de la localidad
    #-----------------------------------------------------

    #Para barrancabermeja celebralo curramba

    modelo += (x[('Barrancabermeja', 'Estados Unidos')] + x[('Barrancabermeja', 'Japon')] + x[('Barrancabermeja', 'Reino Unido')] + x[('Barrancabermeja', 'Canada')]) <= q["Barrancabermeja"]

    #Para Cartagena nojoda

    modelo += (x[('Cartagena', 'Estados Unidos')] + x[('Cartagena', 'Japon')] + x[('Cartagena', 'Reino Unido')] + x[('Cartagena', 'Canada')]) <= q["Cartagena"]

    #Para ortito digo orito

    modelo += (x[('Orito', 'Estados Unidos')] + x[('Orito', 'Japon')] + x[('Orito', 'Reino Unido')] + x[('Orito', 'Canada')]) <= q["Orito"]


    #---------------------------------------------
    # Satisfacer la demanda  anual de los paises
    #---------------------------------------------

    #Para iunaited stei

    modelo += (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Cartagena', 'Estados Unidos')] - x[('Orito', 'Estados Unidos')]) <= -d["Estados Unidos"]

    #Para uwu

    modelo += (-x[('Barrancabermeja', 'Japon')] - x[('Cartagena', 'Japon')] - x[('Orito', 'Japon')]) <= -d["Japon"]

    #Para bloodyhell

    modelo += (-x[('Barrancabermeja', 'Reino Unido')] - x[('Cartagena', 'Reino Unido')] - x[('Orito', 'Reino Unido')]) <= -d["Reino Unido"]

    #para asia en el hemisferio norte

    modelo += (-x[('Barrancabermeja', 'Canada')] - x[('Cartagena', 'Canada')] - x[('Orito', 'Canada')]) <= -d["Canada"]

    #Resolver Problema

    modelo.solve()


    print("Minimizar Costos:\t",modelo.objective.value(),"\n")

    print("\nValores de las variables:")
    for var in modelo.variables():
        print(f"{var.name}: {var.value()}")


    

def modeloIndexado():

    #Creacion Conjuntos

    conjuntosRefinerias = pd.read_excel(io="Punto2.xlsx", sheet_name='Capacidad')

    conjuntosPaises = pd.read_excel(io="Punto2.xlsx", sheet_name='Demanda')

    L = [i for i in conjuntosRefinerias["Refineria"]]

    P = [i for i in conjuntosPaises["Pais"]]

    #Parametros

    capacidad = pd.read_excel(io="Punto2.xlsx", sheet_name="Capacidad",index_col=0).squeeze()
    demanda = pd.read_excel(io="Punto2.xlsx", sheet_name='Demanda',index_col=0).squeeze()
    destino = pd.read_excel(io="Punto2.xlsx", sheet_name='Destino', index_col=(0,1)).squeeze()


    #Capacidad de produccion de crudo en litros de la localidad i

    q = {i:capacidad[i] for i in L if not pd.isna(i)} 

    #Demanda en litros de crudo anuales del pais j

    d = {j:demanda[j] for j in P if not pd.isna(j)} 

    #Costo unitario en pesos para enviar crudo desde la localidad i al pais j

    #print(destino["Barrancabermeja","Estados Unidos"])

    c = {(i,j): destino[(i,j)] for i in L for j in P if not pd.isna(i) and not pd.isna(j)}

    #Problema

    modelo = lp.LpProblem(name="literal A",sense=lp.LpMinimize)

    #Variables Decision

    x={(i,j):lp.LpVariable(f'litros_solicitados_localidad_{i}_para_pais_{j}',lowBound=(0),cat=lp.LpContinuous)for i in L for j in P}
    
    #-----------------------------
    # Función objetivo
    #-----------------------------  

     #Para barrancabermeja celebralo curramba

    modelo += sum(x[(i,j)] - c[(i,j)] for i in L for j in P)

    #Restricciones
    #-----------------------------------------------------
    #No superar la capacidad de produccion de la localidad
    #-----------------------------------------------------

    #Para barrancabermeja celebralo curramba

    for i in L:

        modelo += sum(x[(i,j)] for j in P) <= q[i] 

    #---------------------------------------------
    # Satisfacer la demanda  anual de los paises
    #---------------------------------------------

    #Para barrancabermeja celebralo curramba

    for j in P:
        modelo += sum(-x[(i,j)] for i in L) <= -d[j]

    #Resolver Problema

    modelo.solve()

    print("Minimizar Costos:\t",modelo.objective.value(),"\n")

    print("\nValores de las variables:")
    for var in modelo.variables():
        print(f"{var.name}: {var.value()}")













#Literal b

def dualidadExplicito():
    return None
    



def dualidadIndexado():
    prob = lp.LpProblem("Dual",lp.LpMinimize)


    #Variables

    w_1 = lp.LpVariable("w_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_2 = lp.LpVariable("w_2",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_3 = lp.LpVariable("w_3",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_4 = lp.LpVariable("w_4",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_5 = lp.LpVariable("w_5",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_6 = lp.LpVariable("w_6",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_7 = lp.LpVariable("w_7",lowBound=0, upBound=None, cat=lp.LpContinuous)

    #Restricciones

    prob += w_1 - w_4 >= 1500, "R1"

    prob += w_1 - w_5 >= 2200, "R2"

    prob += w_1 - w_6 >= 2000, "R3"

    prob += w_1 - w_7 >= 1800, "R4"

    prob += w_2 - w_4 >= 1400, "R5"

    prob += w_2 - w_5 >= 2400, "R6"

    prob += w_2 - w_6 >= 1900, "R7"

    prob += w_2 - w_7 >= 2200, "R8"

    prob += w_3 - w_4 >= 2000, "R9"

    prob += w_3 - w_5 >= 2500, "R10"

    prob += w_3 - w_6 >= 2100, "R11"

    prob += w_3 - w_7 >= 1900, "R12"


    #FunObjetivo

    prob += 600000*w_1 + 500000*w_2 + 400000*w_3 - 500000*w_4 -300000*w_5 -200000*w_6 -250000*w_7

    prob.solve()

    #Resultados

    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))


    print("\nvariables: ")
    print(f"w_1 = {lp.value(w_1)}")
    print(f"w_2 = {lp.value(w_2)}")
    print(f"w_3 = {lp.value(w_3)}")
    print(f"w_4 = {lp.value(w_4)}")
    print(f"w_5 = {lp.value(w_5)}")
    print(f"w_6 = {lp.value(w_6)}")
    print(f"w_7 = {lp.value(w_7)}")

    """
    Se puede utilizar la funcion de Pulp para llamar a las restricciones
    directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    (OptiEnv)
    """

    print("\nVariables de holgura: ")
    print(prob.constraints["R1"].slack)
    print(prob.constraints["R2"].slack)
    print(prob.constraints["R3"].slack)
    print(prob.constraints["R4"].slack)
    print(prob.constraints["R5"].slack)
    print(prob.constraints["R6"].slack)
    print(prob.constraints["R7"].slack)
    print(prob.constraints["R8"].slack)
    print(prob.constraints["R9"].slack)
    print(prob.constraints["R10"].slack)
    print(prob.constraints["R11"].slack)
    print(prob.constraints["R12"].slack)



    print("\nVariables duales: ")

    for i in range(1,13):
        print(prob.constraints[f"R{i}"].pi)







print(modeloIndexado())
#print(modeloExplicito())
#print(dualidadExplicito())