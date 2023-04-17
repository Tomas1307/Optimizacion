import matplotlib.pyplot as plt
import pulp as lp

#conjuntos

# fincas
F = [1,2,3,4,5,6,7,8,9,10]

#vehiculos
V=["camion","carro","Moto"]


# parametros


# Audiencia de cada artista en cada hora
k = {1:725,
    2:532,
    3:593,
    4:838,
    5: 821,
    6: 806,
    7: 869,
    8: 788,
    9: 791,
    10: 565}
c = {1:8900000,
    2:8100000,
    3:8500000,
    4:9500000,
    5:9400000,
    6:9200000,
    7: 10000000,
    8: 90000000,
    9: 90000000,
    10: 8200000}

d={1:81,2:69,3:87,4:90,5:94,6:67,7:67,8:71,9:73,10:80}
r={"camion":500,"carro":300,"Moto":250}
b={"camion":200,"carro":125,"Moto":75}
a={"camion":1200000,"carro":800000,"Moto":500000}
n={"camion":1,"carro":2,"Moto":4}

problema = lp.LpProblem(name="punto_2", sense = lp.LpMinimize)

# variables de decision
# Si el artista a en A inicia su presentación en t en H
x =lp.LpVariable.dicts("la finca se usa",[(i)for i in F],0,1,lp.LpBinary)

# Si el artista a en A se presenta durante la hora t in H
y = lp.LpVariable.dicts("canridad a enviar",[(i,j)for i in F for j in V],0,None,lp.LpInteger)
#funcion objetivo
problema += lp.lpSum(c[i] * x[i] for i in F) +lp.lpSum(r[j] * d[i] *y[i,j]for i in F for j in V)+lp.lpSum(a[j] *y[i,j]for i in F for j in V)
#restricciones
for i in F:
    problema += lp.lpSum(b[(j)]*y [(i,j)]for j in V) <= k[i]*x[i]
    problema+=lp.lpSum(c[i]*x[i] for i in F)<=55000000
    problema+=lp.lpSum(b[i]*y[i,j] for i in F for j in V)>=4000
                                                                                              
for i in F:
    if i==2 or i ==8 or i ==10:
       problema+=y[i,"camion"]==0
for i in F:
     for j in V:                                                                                         
       problema+=y[i,j]<=n[j]

problema.solve()

"""
print(f"Estado del optimizador: {lp.LpStatus[problema.status]}")
print(f"costo total:\t",problema.objective.value())
print(f"costo de la adecuacion:\t",sum(c[i]*x[i].varvaruable() for in in F),"\n")


print ( " se usan estas fincas con esta cantidad de vehiculos:\n")
for i in F:
    if x [i]varValue==1:
    print ("..finca",i,"\n")

for j in V:
    if y [i,j]varValue>0:
         print ("..",j,":",y[i,j].varvalue)                                                                         
    print("\n")

print ("total:",sum(b[j]*y[i,j].varvalue for i in F for j in V),"kg")
"""