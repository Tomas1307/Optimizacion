import pulp as lp
import pandas as pd


#file_name = 'Datos.xlsx'


# -----------------
# Conjuntos
# -----------------
# Variable de los conjuntos


def optimizacion(file_name):
    conjuntos = pd.read_excel(io=file_name, sheet_name='Tabla 2.1')
    print(conjuntos)
    F=[]
    V=["Camion","Carro","Moto"]
    #Creacion Conjuntos
    for i in conjuntos['Finca']:
        if not pd.isna(i):
            F.append(i)
            #print(i)
    #print(F)

    

    #Parametros

    #Capacidad de produccion
    k_i = {i:conjuntos['Capacidad de producción [kg]'][i-1] for i in F}
    print(k_i)

    nc=  pd.read_excel(io=file_name, sheet_name='Tabla 2.1',index_col=0).squeeze()

    #Costos

    #c = {i: nc["Costo"][i] for i in P}

    #Creacion del problema

    modelo = lp.LpProblem('Entrenamiento_2', sense = lp.LpMinimize)

    #Variables de decision

print(optimizacion(file_name='Datos.xlsx'))