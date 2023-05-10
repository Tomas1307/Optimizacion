#-------
# AUTHORS
# t.acosta - 202011237
# al.martinezc1 - 202012606
#-------

import pulp as lp
import pandas as pd
from prettytable import PrettyTable

def optimizacion_incisoB():
    G = ["CUPA","PALO","Logistics","BioTech","InvestiObras","AlpesIA"]
    D = [i for i in range(1,7)]
    H = [i for i in range(1,31)]
    
    #Subconjunto derivado de H de los intervalos 
    I = {}
    start = 1
    for i in range(1, 7):
        I[i] = list(range(start, start + 5))
        start += 5  

    #A PARTE SOBRE EL ENUNCIADO
    sesiones =[3,3,4,1,1,1]
    duracion = [2,2,1,3,3,2]

    #Parametros

   
   # Numero de franjas horarias para cada grupo de investigacion en un dia cualquiera
    s = {}
    for i in range(0,len(sesiones)):
        s[G[i]]=sesiones[i]
    print(s)


    #Duracion(franjas horarias) por grupo 
    d={}
    for i in range(0,len(G)):
        d[G[i]]=duracion[i]
    #print(d_i)

    #Numero de franjas horarias en la semana
    franjas_semana_j = {}
    for i in H:
        franjas_semana_j[int(i)] = int((i - 1) % 5 + 1)
    print(franjas_semana_j)

    # Crear el modelo
    modelo = lp.LpProblem("Mi modelo", lp.LpMinimize)

    #Variables decision

    x=lp.LpVariable.dicts("Se encuentra en sesion",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    y=lp.LpVariable.dicts("Sesion empezada",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    z=lp.LpVariable.dicts("Sesion Terminada",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    w=lp.LpVariable("Horario Mayor",0,None,lp.LpInteger)

    modelo+=w

    
    #Restricciones

    for i in G:
        modelo+=lp.lpSum(x[i,k] for k in H)==s[i]*d[i]
        modelo+=lp.lpSum(y[i,k] for k in H)==s[i]
        modelo+=lp.lpSum(z[i,k] for k in H)==s[i]
        modelo+=lp.lpSum(z[i,k]*k for k in H)-lp.lpSum(y[i,k]*k for k in H)==s[i]*(d[i]-1)
        for k in H:
            modelo+=lp.lpSum(x[i,k] for i in G)<=1
            modelo+= w >= z[i,k]*franjas_semana_j[k]
            if k+d[i]-1<=len(H):
                modelo+=lp.lpSum(y[i,f] for f in range(k,k+d[i]))<=1
            if franjas_semana_j[k]+d[i]-1>5:
                modelo+=y[i,k]==0
            if k+d[i]-1<=len(H):
                modelo+=lp.lpSum(x[i,f] for f in range(k,k+d[i]))>=d[i]*y[i,k]
            if k>=d[i]:
                modelo+=lp.lpSum(x[i,f] for f in range(k-d[i]+1,k+1))>=d[i]*z[i,k]
            else:
                modelo+=y[i,k]==0
                modelo+=z[i,k]==0

        for j in D:
            modelo+=lp.lpSum(x[i,j] for j in I[j])<=3
            
    modelo.solve()
    print("Maxima Franja de Finalizar:\t",modelo.objective.value(),"\n")


    # Nueva tabla
    table = PrettyTable()
    table.field_names = ["Dias"] + G

    # Llenar la tabla
    for j in D:
        row = [j]
        for i in G:
            sesion = ""
            for k in I[j]:
                if x[i,k].value() == 1:
                    sesion = i
                    print(sesion)
                    break
            row.append(sesion)
        table.add_row(row)

    print(table)

#Para el inciso e.

def optimizacion_incisoE():
    G = ["CUPA","PALO","Logistics","BioTech","InvestiObras","AlpesIA"]
    D = [i for i in range(1,7)]
    H = [i for i in range(1,31)]
    
    #Subconjunto derivado de H de los intervalos 
    I = {}
    start = 1
    for i in range(1, 7):
        I[i] = list(range(start, start + 5))
        start += 5  

    #A PARTE SOBRE EL ENUNCIADO
    sesiones =[3,3,4,1,1,1]
    duracion = [2,2,1,3,3,2]

    #Parametros

   
   # Numero de franjas horarias para cada grupo de investigacion en un dia cualquiera
    s = {}
    for i in range(0,len(sesiones)):
        s[G[i]]=sesiones[i]
    print(s)


    #Duracion(franjas horarias) por grupo 
    d={}
    for i in range(0,len(G)):
        d[G[i]]=duracion[i]
    #print(d_i)

    #Numero de franjas horarias en la semana
    franjas_semana_j = {}
    for i in H:
        franjas_semana_j[int(i)] = int((i - 1) % 5 + 1)
    print(franjas_semana_j)

    # Crear el modelo
    modelo = lp.LpProblem("Mi modelo", lp.LpMinimize)

    #Variables decision

    x=lp.LpVariable.dicts("Se encuentra en sesion",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    y=lp.LpVariable.dicts("Sesion empezada",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    z=lp.LpVariable.dicts("Sesion Terminada",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    w=lp.LpVariable("Horario Mayor",0,None,lp.LpInteger)
    t=lp.LpVariable.dicts("Ultima sesion del gupo termina en franja horaria",[(i,k) for i in G for k in H],0,1,lp.LpBinary)

    modelo+=w

    
    #Restricciones

    for i in G:
        modelo+=lp.lpSum(x[i,k] for k in H)==s[i]*d[i]
        modelo+=lp.lpSum(y[i,k] for k in H)==s[i]
        modelo+=lp.lpSum(z[i,k] for k in H)==s[i]
        modelo+=lp.lpSum(z[i,k]*k for k in H)-lp.lpSum(y[i,k]*k for k in H)==s[i]*(d[i]-1)
        for k in H:
            modelo+=lp.lpSum(x[i,k] for i in G)<=1
            modelo+= w >= z[i,k]*franjas_semana_j[k]
            #######NUEVA RESTRICCION#########
            modelo += w >= t[i,k] * franjas_semana_j[k]
            #######NUEVA RESTRICCION#########
            if k+d[i]-1<=len(H):
                modelo+=lp.lpSum(y[i,f] for f in range(k,k+d[i]))<=1
            if franjas_semana_j[k]+d[i]-1>5:
                modelo+=y[i,k]==0
            if k+d[i]-1<=len(H):
                modelo+=lp.lpSum(x[i,f] for f in range(k,k+d[i]))>=d[i]*y[i,k]
            if k>=d[i]:
                modelo+=lp.lpSum(x[i,f] for f in range(k-d[i]+1,k+1))>=d[i]*z[i,k]
            else:
                modelo+=y[i,k]==0
                modelo+=z[i,k]==0

        for j in D:
            modelo+=lp.lpSum(x[i,j] for j in I[j])<=3

        #######NUEVA RESTRICCION#########
        modelo += lp.lpSum(z[i,k]*k for i in G for k in H) <= w
        #######NUEVA RESTRICCION#########
            
    modelo.solve()
    print("Maxima Franja de Finalizar:\t",modelo.objective.value(),"\n")


    # Nueva tabla
    table = PrettyTable()
    table.field_names = ["Dias"] + G

    # Llenar la tabla
    for j in D:
        row = [j]
        for i in G:
            sesion = ""
            for k in I[j]:
                if x[i,k].value() == 1:
                    sesion = i
                    print(sesion)
                    break
            row.append(sesion)
        table.add_row(row)

    print(table)

#------------PRUEBAS DE AMBOS INCISOS---------------------

#####PARA PROBAR INCISO B QUITAR EL #
#print(optimizacion_incisoB())
#####PARA PROBAR INCISO E QUITAR EL #
#print(optimizacion_incisoE())

#------------------------------------------------------------
