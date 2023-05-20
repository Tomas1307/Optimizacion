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

    # Se crea diccionario para guardar las restricciones
    resultados = dict()



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

def optiPetsDesplazada():
    # lista donde se guardarán los resultados de cada iteración
    res = []
    # valor de la variable dual
    dual = 1
    # contador de iteraciones una vez la dual alcanza el valor de 0
    l = 0
    # Valor del lado derecho de la restricción R3
    b = 0

    conjuntos = pd.read_excel(io="Punto2.xlsx", sheet_name='Sensibilidad')

    I = [i for i in conjuntos["Insumo"]] 
    T = ["Cachorro","Adulto"]
    #Tiempos procesamiento kg
    tiempo = [2,3]

    #P
    cantidad = pd.read_excel(io="Punto2.xlsx", sheet_name='Sensibilidad',index_col=0).squeeze()
    produccion = pd.read_excel(io="Punto2.xlsx", sheet_name='Produccion',index_col=(0,1)).squeeze()

    # Parametros

    #Disponibilidad semanal del ingrediente
    d = {i: cantidad[i] for i in I if not pd.isna(i)}
    
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

    while l < 3 or dual > 0:
        #Creacion Problema

        prob = lp.LpProblem("Punto3",sense= lp.LpMaximize)

        #Variables

        x={j:lp.LpVariable(f'cantidad_producida_para_{j}',lowBound=(0),cat=lp.LpContinuous)for j in T}
        
        #Restricciones

        # Se crea diccionario para guardar las restricciones
        resultados = dict()



        #No superar horas maximas de produccion

        prob += sum(x[j] * t[j] for j in T) <= h, "R1"

        #No superar la disponibilidad del tipo de producto

        for i in I:
            prob += sum(x[j] * k[(j,i)] for j in T) <= d[i], f"R2_{i}"

        #No superar la capacidad de produccion

            prob += sum(x[j] for j in T) <= c + b, f"R3_{i}"

        #Funcion Objetivo

            prob += sum(x[j] * u[j] for j in T), "R4"

        #Solucionar

        prob.solve()

        dual = prob.constraints[f"R3_Pollo"].pi

        results = "Minimizar Costos:\t" + str(prob.objective.value())
        results += "\nValores de las variables:\n"

        for var in prob.variables():
            results += f"{var.name}: {var.value()}\n"


        resultados["Dual"] = dual
        resultados["F.O"] = lp.value(prob.objective)
        for var in prob.variables():
            resultados[var.name] = var.value
        resultados["b"] = b

        # Guardar el diccionario en la lista de soluciones

        res += [resultados]
        

        # Aumentar el valor del lado derecho de la restricción
        # para la siguiente iteración
        
        b += 100

        # Evaluar si la dual ya es 0 y aumentar número de iteración
        
        
        l += 1

    # Dar formato de tabla a los resultados con la librería "Pandas"
    # Guardar la tabla en el objeto "df"

    print("iteraciones",l )
    df = pd.DataFrame(res)
    # Visualizar cómo luce la tabla
    print(df)

    #*-------*-------*
    #Imprimir Gráfica
    #*-------*-------*

    #Crear gráfica y sub-gráfica que sobrelapa a la primera y aporta los
    #títulos a los ejes
    fig, gra = plt.subplots()

    #Indicamos qué info va en el eje "x" y en el "y"
    plt.plot(df["b"], df["F.O"])

    #Dar formato a la gráfica
    gra.set(xlabel = 'Recurso',ylabel= 'Valor F.O',title='F.O vs Recurso R3')
    plt.grid()

    #Mostrar gráfica
    plt.show()


    


print(optiPetsDesplazada())