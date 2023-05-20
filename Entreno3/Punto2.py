#-------
# AUTHORS
# t.acosta - 202011237
# l.guerrerom - 202021248 
#-------

import pulp as lp
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def solve_model_index():
    file_path = "Punto2.xlsx"
    
    try:
        # Creacion Conjuntos
        conjuntosRefinerias = pd.read_excel(io=file_path, sheet_name='Capacidad')
        conjuntosPaises = pd.read_excel(io=file_path, sheet_name='Demanda')
        L = [i for i in conjuntosRefinerias["Refineria"]]
        P = [i for i in conjuntosPaises["Pais"]]

        # Parametros
        capacidad = pd.read_excel(io=file_path, sheet_name="Capacidad", index_col=0).squeeze()
        demanda = pd.read_excel(io=file_path, sheet_name='Demanda', index_col=0).squeeze()
        destino = pd.read_excel(io=file_path, sheet_name='Destino', index_col=(0, 1)).squeeze()

        # Capacidad de produccion de crudo en litros de la localidad i
        q = {i: capacidad[i] for i in L if not pd.isna(i)}

        # Demanda en litros de crudo anuales del pais j
        d = {j: demanda[j] for j in P if not pd.isna(j)}

        # Costo unitario en pesos para enviar crudo desde la localidad i al pais j
        c = {(i, j): destino[(i, j)] for i in L for j in P if not pd.isna(i) and not pd.isna(j)}

        # Problema
        modelo = lp.LpProblem(name="literal A", sense=lp.LpMinimize)

        # Variables Decision
        x = {(i, j): lp.LpVariable(f'litros_{i}_para_{j}', lowBound=0, cat=lp.LpContinuous)
             for i in L for j in P}

        # Función objetivo
        modelo += sum(x[(i, j)] * c[(i, j)] for i in L for j in P)

        # Restricciones
        for i in L:
            modelo += sum(x[(i, j)] for j in P) <= q[i]

        for j in P:
            modelo += sum(-x[(i, j)] for i in L) <= -d[j]

        # Resolver Problema
        modelo.solve()

        # Mostrar resultados en una ventana de mensaje
        results = "Minimizar Costos:\t" + str(modelo.objective.value()) + "\n\nValores de las variables:\n"
        for var in modelo.variables():
            results += f"{var.name}: {var.value()}\n"


        messagebox.showinfo("Resultados", results)

    except Exception as e:
        messagebox.showerror("Error", "Se produjo un error al resolver el modelo: " + str(e))


def solve_model_explicit():
    #Creacion Conjuntos

    try:

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

        x={(i,j):lp.LpVariable(f'litros_{i}_para_{j}',lowBound=(0),cat=lp.LpContinuous)for i in L for j in P}

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

        results = "Minimizar Costos:\t" + str(modelo.objective.value())
        results += "\nValores de las variables:\n"

        for var in modelo.variables():
            results += f"{var.name}: {var.value()}\n"

   

        messagebox.showinfo("Resultados", results)

    except Exception as e:
        messagebox.showerror("Error", "Se produjo un error al resolver el modelo: " + str(e))


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
    results = "Estado: " + lp.LpStatus[prob.status] + "\n"
    results += "El valor de la F.O. es: " + str(lp.value(prob.objective)) + "\n\n"

    results += "Variables:\n"
    for var in W:
        results += f"{var} = {lp.value(W[var])}\n"

    results += "\nVariables de holgura:\n"
    for i in range(1, 13):
        results += f"s_{i} = " + str(prob.constraints[f"R{i}"].slack) + "\n"

    results += "\nVariables duales:\n"
    for i in range(1, 13):
        results += f"x_{i} = " + str(prob.constraints[f"R{i}"].pi) + "\n"

    messagebox.showinfo("Resultados", results)


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

    results = "Estado: " + lp.LpStatus[prob.status] + "\n"
    results += "El valor de la F.O. es: " + str(lp.value(prob.objective)) + "\n\n"

    results += f"w_1 = {lp.value(w_1)} \n"
    results += f"w_2 = {lp.value(w_2)} \n"
    results += f"w_3 = {lp.value(w_3)} \n"
    results += f"w_4 = {lp.value(w_4)} \n"
    results += f"w_5 = {lp.value(w_5)} \n"
    results += f"w_6 = {lp.value(w_6)} \n"
    results += f"w_7 = {lp.value(w_7)} \n"



    results += "\nVariables de holgura:\n"
    for i in range(1, 13):
        results += f"s_{i} = " + str(prob.constraints[f"R{i}"].slack) + "\n"

    results += "\nVariables duales: \n "

    for i in range(1,13):
        results += f"x_{i} = " + str(prob.constraints[f"R{i}"].pi) + "\n"

    messagebox.showinfo("Resultados", results)
#
#
##
#
#
#A LA HORA DE EJECUTARLO SOLO SE DEBE PRESIONAR RUN Y SELECCIONAR EL MODELO QUE SE DESEA VER.
#
#
##
#
#
def create_interface():
    window = tk.Tk()
    window.title("Interfaz para dualidad")

    window.geometry("300x200")


    
    
    solve_button = tk.Button(window, text="Modelo Primal Indexado", command=solve_model_index)

    solve_button2 = tk.Button(window, text="Modelo Primal Explicito", command=solve_model_explicit)

    solve_button3 = tk.Button(window, text="Modelo Dual Indexado", command=dualidadIndexado)

    solve_button4 = tk.Button(window, text="Modelo Dual Explicito", command=dualidadExplicito)


    solve_button.pack(pady=10)
    solve_button2.pack(pady=10)
    solve_button3.pack(pady=10)   
    solve_button4.pack(pady=10)  
    window.mainloop()

create_interface()