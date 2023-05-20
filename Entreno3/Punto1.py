#-------
# AUTHORS
# t.acosta - 202011237
# l.guerrerom - 202021248 
#-------
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

    R1Barranca = x[('Barrancabermeja', 'Estados Unidos')] * c[('Barrancabermeja', 'Estados Unidos')] + x[('Barrancabermeja', 'Japon')] * c[('Barrancabermeja', 'Japon')] + x[('Barrancabermeja', 'Reino Unido')] * c[('Barrancabermeja', 'Reino Unido')]+ x[('Barrancabermeja', 'Canada')] * c[('Barrancabermeja', 'Canada')]

    #Para Cartagena nojoda

    R1Cartagena = x[('Cartagena', 'Estados Unidos')] * c[('Cartagena', 'Estados Unidos')] + x[('Cartagena', 'Japon')] * c[('Cartagena', 'Japon')]+ x[('Cartagena', 'Reino Unido')] * c[('Cartagena', 'Reino Unido')] + x[('Cartagena', 'Canada')] * c[('Cartagena', 'Canada')]

    #Para ortito digo Orito

    R1Orito = x[('Orito', 'Estados Unidos')] * c[('Orito', 'Estados Unidos')]+ x[('Orito', 'Japon')] * c[('Orito', 'Japon')]+ x[('Orito', 'Reino Unido')] * c[('Orito', 'Reino Unido')]+ x[('Orito', 'Canada')] * c[('Orito', 'Canada')]

    modelo += R1Barranca + R1Cartagena + R1Orito

    #Restricciones
    #-----------------------------------------------------
    #No superar la capacidad de produccion de la localidad
    #-----------------------------------------------------

    #Para compadre ando con una arrechera que si uste me dice voy a bogota

    modelo += (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')]) >= -q["Barrancabermeja"]

    #Para Cartagena nojoda

    modelo += (-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]) >= -q["Cartagena"]

    #Para ortito digo orito

    modelo += (-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]) >= -q["Orito"]


    #---------------------------------------------
    # Satisfacer la demanda  anual de los paises
    #---------------------------------------------

    #Para mejico primium

    modelo += (x[('Barrancabermeja', 'Estados Unidos')] + x[('Cartagena', 'Estados Unidos')] + x[('Orito', 'Estados Unidos')]) >= d["Estados Unidos"]

    #Para uwu

    modelo += (x[('Barrancabermeja', 'Japon')] + x[('Cartagena', 'Japon')] + x[('Orito', 'Japon')]) >= d["Japon"]

    #Para bloodyhell

    modelo += (x[('Barrancabermeja', 'Reino Unido')] + x[('Cartagena', 'Reino Unido')] + x[('Orito', 'Reino Unido')]) >= d["Reino Unido"]

    #para asia en el hemisferio norte

    modelo += (x[('Barrancabermeja', 'Canada')] + x[('Cartagena', 'Canada')] + x[('Orito', 'Canada')]) >= d["Canada"]

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

    modelo += sum(x[(i,j)] * c[(i,j)] for i in L for j in P)

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

    print("Status", lp.LpStatus[modelo.status])

    print("\nValores de las variables:")
    for var in modelo.variables():
        print(f"{var.name}: {var.value()}")

