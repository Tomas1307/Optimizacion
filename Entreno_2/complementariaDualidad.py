import pulp as lp

##Objeto Problema

def primal():

    prob = lp.LpProblem("primal",lp.LpMaximize)


    #Variables

    x_1 = lp.LpVariable("x_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    x_2 = lp.LpVariable("x_2",lowBound=0, upBound=None, cat=lp.LpContinuous)

    #Restricciones

    prob += x_1 + 2 * x_2 <= 8, "R1"

    prob += -x_1 -7 * x_2 <= -14, "R2"

    prob += x_1 - x_2 <= 1, "R3"

    prob += 1/20 *x_1 -x_2 <= -1.3, "R4"


    #FunObjetivo

    prob += 2 * x_1 -3 *x_2

    prob.solve()

    #Resultados

    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))


    print("\nvariables: ")
    print(f"x_1 = {lp.value(x_1)}")
    print(f"x_2 = {lp.value(x_2)}")

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

    print("\nVariables duales: ")

    for i in range(1,5):
        print(prob.constraints[f"R{i}"].pi)


def dual():

    prob = lp.LpProblem("Dual",lp.LpMinimize)


    #Variables

    w_1 = lp.LpVariable("w_1",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_2 = lp.LpVariable("w_2",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_3 = lp.LpVariable("w_3",lowBound=0, upBound=None, cat=lp.LpContinuous)
    w_4 = lp.LpVariable("w_4",lowBound=0, upBound=None, cat=lp.LpContinuous)

    #Restricciones

    prob += w_1 - w_2 + w_3 + 1/20 * w_4 >= 2, "R1"

    prob += 2*w_1 - 7*w_2 - w_3 - w_4 >= -3 , "R2"



    #FunObjetivo

    prob += 8*w_1 -14*w_2 + w_3 -1.3*w_4 

    prob.solve()

    #Resultados

    print("Estado: ", lp.LpStatus[prob.status])
    print("El valor de la F.O. es: ", lp.value(prob.objective))


    print("\nvariables: ")
    print(f"w_1 = {lp.value(w_1)}")
    print(f"w_2 = {lp.value(w_2)}")
    print(f"w_3 = {lp.value(w_3)}")
    print(f"w_4 = {lp.value(w_4)}")

    """
    Se puede utilizar la funcion de Pulp para llamar a las restricciones
    directamente por el nombre dado y luego obtener la dual asociada

    print(prob.constraints["R1"])
    (OptiEnv)
    """

    print("\nVariables de holgura: ")
    print(prob.constraints["R1"].slack)
    print(prob.constraints["R2"].slack)


    print("\nVariables duales: ")

    for i in range(1,3):
        print(prob.constraints[f"R{i}"].pi)

print(dual())