import pulp as lp
import pandas as pd


#file_name = 'Datos.xlsx'


# -----------------
# Conjuntos
# -----------------
# Variable de los conjuntos


def optimizacion():
    G = ["CUPA","PALO","Logistics","BioTech","InvestiObras","AlpesIA"]
    D = [i for i in range(1,7)]
    H = [_ for _ in range(1,31)]
    
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
    s_i = {}
    for i in range(0,len(sesiones)):
        s_i[G[i]]=sesiones[i]
    #print(s_i)


    #Duracion(franjas horarias) por grupo 
    d_i={} #d
    for i in range(0,len(G)):
        d_i[G[i]]=duracion[i]
    #print(d_i)

    #Numero de franjas horarias en la semana
    franjas_semana_j = {}
    for i in H:
        franjas_semana_j[i] = (i - 1) % 5 + 1
    #print(franjas_semana_j)

    # Crear el modelo
    modelo = lp.LpProblem("Mi modelo", lp.LpMinimize)

    #Variables decision

    x=lp.LpVariable.dicts("Está en Sesión?",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    y=lp.LpVariable.dicts("Empieza Sesión?",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    z=lp.LpVariable.dicts("Termina Sesión?",[(i,k) for i in G for k in H],0,1,lp.LpBinary)
    w=lp.LpVariable("Horario de Salida Mayor",0,None,lp.LpInteger)

    # Restricción 1: Cada grupo debe tener exactamente s_i franjas de duración d_i asignadas
    for i in G:
        modelo+=lp.lpSum(x[i,j] for j in H)==d_i[i]*s_i[i]
    for i in G:
        modelo+=lp.lpSum(y[i,j] for j in H)==d_i[i]
    for i in G:
        modelo+=lp.lpSum(z[i,j] for j in H)==d_i[i]
        
    for i in G:
        for j in H:
            if j+s_i[i]-1<=len(H):
                modelo+=lp.lpSum(y[i,f] for f in range(j,j+s_i[i]))<=1

    for j in H:
        modelo+=lp.lpSum(x[i,j] for i in G)<=1

    for i in G:
        for k in D:
            modelo+=lp.lpSum(x[i,j] for j in I[k])<=3
        
    for i in G:
        for j in H:
            if franjas_semana_j[j]+s_i[i]-1>5:
                modelo+=y[i,j]==0
                
    for i in G:
        modelo+=lp.lpSum(z[i,j]*j for j in H)-lp.lpSum(y[i,j]*j for j in H)==d_i[i]*(s_i[i]-1)

    for i in G:
        for j in H:
            if j+s_i[i]-1<=len(H):
                modelo+=lp.lpSum(x[i,f] for f in range(j,j+s_i[i]))>=s_i[i]*y[i,j]
            else:
                modelo+=y[i,j]==0

    for i in G:
        for j in H:
            if j>=s_i[i]:
                modelo+=lp.lpSum(x[i,f] for f in range(j-s_i[i]+1,j+1))>=s_i[i]*z[i,j]
            else:
                modelo+=z[i,j]==0

    for i in G:
        for j in H:
            modelo+=w>=z[i,j]*franjas_semana_j[j]

    modelo.solve()
    print("Máxima Franja de Finalización:\t",modelo.objective.value(),"\n")


    for j in H:
        print(j,"\t",end="")
        Grupo="-----"
        for i in G:
            if x[i,j].varValue==1:
                Grupo=i
        print(Grupo)

print(optimizacion())