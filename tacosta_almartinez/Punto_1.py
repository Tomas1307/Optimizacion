#-------
# AUTHORS
# t.acosta - 202011237
# al.martinezc1 - 202012606
#-------

import pulp as lp
import pandas as pd

# Guardar nombre del archivo en una variable
file_name = 'Datos.xlsx'

# -----------------
# Conjuntos
# -----------------

# Variable de los conjuntos
conjuntos = pd.read_excel(io=file_name, sheet_name='Tabla 1.1')

# Medicamentos
P = [i for i in conjuntos['Medicamentos'] if not pd.isna(i)]

# Malestares
M = [i for i in conjuntos['Enfermedad'] if not pd.isna(i)]

# -----------------
# Parámetros
# -----------------


# Parámetro k
R=85000000

# Costo fijo de montaje
cos_a = pd.read_excel(io=file_name, sheet_name='Tabla 1.1', index_col=0).squeeze()
c_i = {i:cos_a['Costo'][i] for i in P}


# -------------------------------------
# Creación del objeto problema en PuLP
# -------------------------------------

modelo = lp.LpProblem('punto_1', sense = lp.LpMaximize)

#variable de decision
x={i:lp.LpVariable(f'´Medicamentos_{i}',lowBound=(0),cat=lp.LpBinary)for i in P}

#restricciones
#maximo dos medicamentos para malestar cardiovascular
for i in P:
        if i =="Cardiovascular":
                i<=2                                                         
#mas de un medicamento asociado a malestar digestivo
for i in P:
    if i== "Digestivos":
        i>=1
#modelo+=lp.lpSum(x[i]for i in conjuntos.loc[conjuntos['Enfermedad']=='Digestivos','Medicamentos'])>=1
#si se compraMetacarbamol se compra ibuprofeno
modelo+=x['Ibuprofeno']>=x['Metacarbamol']
#si se compra rifaximina o Loperamida o los dos se compra Enterogermina
modelo+=x['Enterogermina']>=x['Rifaximina']
modelo+=x['Enterogermina']>=x['Loperamida']
#si se compra Naproxeno y Diezepam,se compra Loratadina o Deslotaradina
modelo+=x['Loratadina']+x['Desloratadina']>=x['Naproxeno']+x['Diezepam']-1
#si se compra Levocetirizina o Desloratadina,se compra Naproxeno o Aspirina
modelo+=x['Naproxeno']+x['Aspirina']>=x['Levocetirizina']+x['Desloratadina']
#si se compra Doxiciclina no se compra Centirizina
modelo+=x['Doxiciclina']+x['Cetirizina']<=1
#respetar el presupuesto
modelo+=lp.lpSum(x[i]*c_i[i] for i in P)<=R
#funcion objetivo
modelo+=lp.lpSum(x[i] for i in P)

#optimizar modelo
modelo.solve(lp.PULP_CBC_CMD(msg=0))
print(f'El status es: {lp.LpStatus[modelo.status]}')

# Valor de la función objetivo
print(f'El objetivo es: {lp.value(modelo.objective)}')

# -----------------------------
#    Imprimir resultados de las variables
# -----------------------------
print('\nResultados:')
for i in P:
    if x[i].varValue==1:
        print(f'Se oferta el medicamento {i}')