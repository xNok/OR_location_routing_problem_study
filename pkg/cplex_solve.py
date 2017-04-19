import cplex

def cplex_solve(obj,ub,lb,colnames,types, rows, senses, rhs, minimize=True, path=None):
    #####################################################################
    # Creating problem
    prob = cplex.Cplex()
    ## Objective function sense
    if minimize:
        prob.objective.set_sense(prob.objective.sense.minimize)
    else:
        prob.objective.set_sense(prob.objective.sense.maximize)
    ## Objective function
    prob.variables.add(obj=obj,ub=ub,lb=lb,names=colnames,types=types)
    ## Constraintes
    prob.linear_constraints.add(lin_expr=rows,senses=senses, rhs=rhs)

    #####################################################################
    # Saving the linear problem formulation into a file
    if path:
        prob.write(path) # print the formulation into a file

    #####################################################################
    # Solving problem
    prob.solve()
    
    return prob