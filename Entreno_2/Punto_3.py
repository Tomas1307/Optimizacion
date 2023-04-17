import pulp as lp
import pandas as pd


#file_name = 'Datos.xlsx'


# -----------------
# Conjuntos
# -----------------
# Variable de los conjuntos


def optimizacion(file_name):
    G = ["CUPA","PALO","Logistics","BioTech","InvestiObras","AlpesIA"]
    D = ["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"]
    H = [2,2,1,3,3,2]
    franjas = ["6:00am - 8:30am","8:30am a 11:00am","11:00AM - 1:30pm ","1:30pm -4:00pm","4:00pm - 6:30pm"]
    #Parametros

    #Cantidad de franjas horarias del grupo 
    c_ij={}
    for i in range(0,len(G)):
        c_ij[G[i]]=H[i]
    #print(c_ij)
   
    d_k = {}
    for i in range(0,len(franjas)):
        d_k[franjas[i]]=2.5
    print(d_k)
    #Creacion del problema

    modelo = lp.LpProblem('Entrenamiento_2', sense = lp.LpMinimize)

    #Variables de decision

print(optimizacion(file_name='Datos.xlsx'))