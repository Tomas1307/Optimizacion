#---------
# Authors
#----------
#Tomas Acosta Bernal
# Luis Guerrero
#---------
import pulp as lp

import matplotlib.pyplot as plp

import pandas as pd

def dualidadIndexado():
    prob = lp.LpProblem("Dual", lp.LpMaximize)

    #Conjuntos

    destino = pd.read_excel(io="Punto2.xlsx", sheet_name='Destino').squeeze()

    D = [i for i in destino["Valor"]]

    R = [(f"w_{i}", f"w_{j}") for i in range(1, 4) for j in range(4, 8)]

    C = [(-1,1) for _ in range(1,13)]

    
    # Variables

    W = {}
    for i in range(1, 8):
        W[f"w_{i}"] = lp.LpVariable(f"w_{i}", lowBound=0, upBound=None, cat=lp.LpContinuous)

    # Restricciones

    restricciones = {}

    for i in range(1,13):

        restricciones[i] = {"variables": R[i-1], "coeficientes": C[i-1], "rhs": D[i-1]}            
        variables_list = restricciones[i]["variables"]
        coeficientes_list = restricciones[i]["coeficientes"]
        rhs = restricciones[i]["rhs"]
        prob += lp.lpSum(coef * W[var] for coef, var in zip(coeficientes_list, variables_list)) <= rhs, f"R{i}"
        
    # Función objetivo
    
    prob += -600000 * W["w_1"] - 500000 * W["w_2"] - 400000 * W["w_3"] + 500000 * W["w_4"] + 300000 * W["w_5"] + 200000 * W["w_6"] + 250000 * W["w_7"]

    prob.solve()

    # Resultados
    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))

    print("\nVariables:")
    for var in W:
        print(f"{var} = {lp.value(W[var])}")

    """
    Se puede utilizar la funcion de Pulp para llamar a las restricciones
    directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    (OptiEnv)
    """

    print("\nVariables de holgura:")
    for i in range(1, 13):
        print(prob.constraints[f"R{i}"].slack)

    print("\nVariables duales:")
    for i in range(1, 13):
        print(prob.constraints[f"R{i}"].pi)

    print("Status", lp.LpStatus[prob.status])


"""

def dualidadExplicito():

    prob = lp.LpProblem("Dual",lp.LpMaximize)

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

    modelo = lp.LpProblem(name="literal A",sense=lp.LpMaximize)

    #Variables Decision

    x={(i,j):lp.LpVariable(f'litros_{i}_para_{j}',lowBound=(0),cat=lp.LpContinuous)for i in L for j in P}


    #Restricciones
    print("AQUIIIIIIIIIIIII", c[("Barrancabermeja","Canada")] )


    #Barranca
    prob += (-1* (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')]) + (
        x[('Barrancabermeja', 'Estados Unidos')] + x[('Cartagena', 'Estados Unidos')] + x[('Orito', 'Estados Unidos')])) <= c[("Barrancabermeja","Estados Unidos")], "R1"
    
    prob += (-1* (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')]) + (
        x[('Barrancabermeja', 'Japon')] + x[('Cartagena', 'Japon')] + x[('Orito', 'Japon')])) <= c[("Barrancabermeja","Japon")], "R2"
    
    prob += (-1* (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')]) + (
        x[('Barrancabermeja', 'Reino Unido')] + x[('Cartagena', 'Reino Unido')] + x[('Orito', 'Reino Unido')])) <= c[("Barrancabermeja","Reino Unido")], "R3"
    
    prob += (-1* (-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')]) + (
        x[('Barrancabermeja', 'Canada')] + x[('Cartagena', 'Canada')] + x[('Orito', 'Canada')])) <= c[("Barrancabermeja","Canada")], "R4"


    #Cartagena

    prob +=  ((-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]) + (
        x[('Barrancabermeja', 'Estados Unidos')] + x[('Cartagena', 'Estados Unidos')] + x[('Orito', 'Estados Unidos')])) <= c[("Cartagena","Estados Unidos")], "R5"
    
    prob += ((-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]) + (
        x[('Barrancabermeja', 'Japon')] + x[('Cartagena', 'Japon')] + x[('Orito', 'Japon')])) <= c[("Cartagena","Japon")], "R6"
    
    prob += ((-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]) + (
        x[('Barrancabermeja', 'Reino Unido')] + x[('Cartagena', 'Reino Unido')] + x[('Orito', 'Reino Unido')])) <= c[("Cartagena","Reino Unido")], "R7"
    
    prob += ((-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]) + (
        x[('Barrancabermeja', 'Canada')] + x[('Cartagena', 'Canada')] + x[('Orito', 'Canada')])) <= c[("Cartagena","Canada")], "R8"
    
    #Orito

    prob += ((-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]) + (
        x[('Barrancabermeja', 'Estados Unidos')] + x[('Cartagena', 'Estados Unidos')] + x[('Orito', 'Estados Unidos')])) <= c[("Orito","Estados Unidos")], "R9"
    
    prob += ((-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]) + (
        x[('Barrancabermeja', 'Japon')] + x[('Cartagena', 'Japon')] + x[('Orito', 'Japon')])) <= c[("Orito","Japon")], "R10"
    
    prob += ((-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]) + (
        x[('Barrancabermeja', 'Reino Unido')] + x[('Cartagena', 'Reino Unido')] + x[('Orito', 'Reino Unido')])) <= c[("Orito","Reino Unido")], "R11"
    
    prob += ((-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]) + (
        x[('Barrancabermeja', 'Canada')] + x[('Cartagena', 'Canada')] + x[('Orito', 'Canada')])) <= c[("Orito","Canada")], "R12"


    #FunObjetivo

    prob += -1 * q["Barrancabermeja"]*(-x[('Barrancabermeja', 'Estados Unidos')] - x[('Barrancabermeja', 'Japon')] - x[('Barrancabermeja', 'Reino Unido')] - x[('Barrancabermeja', 'Canada')])
    + (-1* q["Cartagena"]*(-x[('Cartagena', 'Estados Unidos')] - x[('Cartagena', 'Japon')] - x[('Cartagena', 'Reino Unido')] - x[('Cartagena', 'Canada')]))
    + (-1 *q["Orito"] * (-x[('Orito', 'Estados Unidos')] - x[('Orito', 'Japon')] - x[('Orito', 'Reino Unido')] - x[('Orito', 'Canada')]))
    + (d["Estados Unidos"]*(x[('Barrancabermeja', 'Estados Unidos')] + x[('Cartagena', 'Estados Unidos')] + x[('Orito', 'Estados Unidos')]))
    + (d["Japon"] * (x[('Barrancabermeja', 'Japon')] + x[('Cartagena', 'Japon')] + x[('Orito', 'Japon')]))
    + (d["Reino Unido"]* (x[('Barrancabermeja', 'Reino Unido')] + x[('Cartagena', 'Reino Unido')] + x[('Orito', 'Reino Unido')]))
    + (d["Canada"]* (x[('Barrancabermeja', 'Canada')] + x[('Cartagena', 'Canada')] + x[('Orito', 'Canada')]) <= c[("Orito","Canada")])

    prob.solve()

    #Resultados

    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))


    for var in modelo.variables():
        print(f"{var.name}: {var.value()}")

    
    #Se puede utilizar la funcion de Pulp para llamar a las restricciones
    #directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    #(OptiEnv)
    

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

    print("Status", lp.LpStatus[prob.status])

"""

def dualidadExplicito():

    prob = lp.LpProblem("Dual",lp.LpMaximize)

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

    modelo = lp.LpProblem(name="literal A",sense=lp.LpMaximize)

    #Variables Decision

    w_1 = lp.LpVariable("w_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_2 = lp.LpVariable("w_2",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_3 = lp.LpVariable("w_3",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_4 = lp.LpVariable("w_4",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_5 = lp.LpVariable("w_5",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_6 = lp.LpVariable("w_6",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_7 = lp.LpVariable("w_7",lowBound=0, upBound=None, cat=lp.LpContinuous)


    print (w_1, "AQUIIIIIIIIIIIIIIIIIIIIIIIII")

    #Restricciones

    prob += -w_1 + w_4 <= c[("Barrancabermeja","Estados Unidos")], "R1"
    prob += -w_1 + w_5 <= c[("Barrancabermeja","Japon")], "R2"
    prob += -w_1 + w_6 <= c[("Barrancabermeja","Reino Unido")], "R3"
    prob += -w_1 + w_7 <= c[("Barrancabermeja","Canada")], "R4"
    prob += -w_2 + w_4 <= c[("Cartagena","Estados Unidos")], "R5"
    prob += -w_2 + w_5 <= c[("Cartagena","Japon")], "R6"
    prob += -w_2 + w_6 <= c[("Cartagena","Reino Unido")], "R7"
    prob += -w_2 + w_7 <= c[("Cartagena","Canada")], "R8"
    prob += -w_3 + w_4 <= c[("Orito","Estados Unidos")], "R9"
    prob += -w_3 + w_5 <= c[("Orito","Japon")], "R10"
    prob += -w_3 + w_6 <= c[("Orito","Reino Unido")], "R11"
    prob += -w_3 + w_7 <= c[("Orito","Canada")], "R12"


    #FunObjetivo

    prob += -q["Barrancabermeja"]*w_1 - q["Cartagena"]*w_2 - q["Orito"]*w_3 + d["Estados Unidos"]*w_4 +d["Japon"]*w_5 +d["Reino Unido"]*w_6 +d["Canada"]*w_7

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

    print("Status", lp.LpStatus[prob.status])


print(dualidadExplicito())

