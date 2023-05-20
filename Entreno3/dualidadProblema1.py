import pulp as lp

##Objeto Problema

def primal():

    prob = lp.LpProblem("primal",lp.LpMaximize)


    #Variables

    x_1 = lp.LpVariable("x_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    x_2 = lp.LpVariable("x_2",lowBound=0, upBound=None, cat=lp.LpContinuous)
    x_3 = lp.LpVariable("x_3",lowBound=0, upBound=None, cat=lp.LpContinuous)
    x_4 = lp.LpVariable("x_4",lowBound=0, upBound=None, cat=lp.LpContinuous)
    x_5 = lp.LpVariable("x_5",lowBound=0, upBound=None, cat=lp.LpContinuous)




    #Restricciones

    prob += 17*x_1 + 20*x_3 <= 150, "R1"

    prob += -13*x_2 -19 * x_4 <= -300, "R2"

    prob += x_1 + x_2+ x_3+ x_4 <= 100, "R3"

    prob += 2*x_1 + x_2+ 4*x_3+ 3*x_4 <= 600, "R4"

    prob += 10*x_2 + 15*x_3+ x_5 <= 275, "R5"

    prob += 3*x_4 <= 75, "R6"


    #FunObjetivo

    prob += 25* x_1 +32 *x_2 + 15*x_3 - 12*x_4 - x_5

    prob.solve()

    #Resultados

    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))


    print("\nvariables: ")
    print(f"x_1 = {lp.value(x_1)}")
    print(f"x_2 = {lp.value(x_2)}")
    print(f"x_3 = {lp.value(x_3)}")
    print(f"x_4 = {lp.value(x_4)}")
    print(f"x_5 = {lp.value(x_5)}")


    """
    Se puede utilizar la funcion de Pulp para llamar a las restricciones
    directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    (OptiEnv)
    """

    print("\nVariables de holgura: ")
    print(prob.constraints["R1"].slack)
    print(prob.constraints["R2"].slack)
    print(prob.constraints["R3"].slack)
    print(prob.constraints["R4"].slack)
    print(prob.constraints["R5"].slack)
    print(prob.constraints["R6"].slack)

    print("\nVariables duales: ")

    for i in range(1,7):
        print(prob.constraints[f"R{i}"].pi)


def dual():

    prob = lp.LpProblem("Dual",lp.LpMinimize)


    #Variables

    w_1 = lp.LpVariable("w_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_2 = lp.LpVariable("w_2",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_3 = lp.LpVariable("w_3",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_4 = lp.LpVariable("w_4",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_5 = lp.LpVariable("w_5",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_6 = lp.LpVariable("w_6",lowBound=0, upBound=None, cat=lp.LpContinuous)


    #Restricciones

    prob += 17*w_1 + w_3 + 2*w_4 >= 25, "R1"

    prob += -13*w_2 + w_3 + w_4 + 10*w_5 >= 32 , "R2"

    prob += 20*w_1 + w_3 + 4*w_4 + 15*w_5 >= 15 , "R3"
    
    prob += -19*w_2 + w_3 + 3*w_4 + 3*w_6 >= -12 , "R4"
    
    prob += w_5  >= -1 , "R5"



    #FunObjetivo

    prob += 150*w_1+-300*w_2+100*w_3+600*w_4 +275*w_5 +75*w_6

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

    """
    Se puede utilizar la funcion de Pulp para llamar a las restricciones
    directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    (OptiEnv)
    """

    print("\nVariables de holgura: ")
    print(prob.constraints["R1"].slack)
    print(prob.constraints["R2"].slack)
    print(prob.constraints["R3"].slack)
    print(prob.constraints["R4"].slack)
    print(prob.constraints["R5"].slack)

    print("\nVariables duales: ")

    for i in range(1,6):
        print(prob.constraints[f"R{i}"].pi)

#print("Primal",primal())
print("Dual",dual())