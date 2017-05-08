import cplex

def cplex_solve(variables,constraints, minimize=True, path=None, verbose=False):
    
    #####################################################################
    # Extract variables
    obj = [];ub = [];lb = [];colnames = [];types = [];
    for v in variables:
        obj      = obj + v["coef"]
        ub       = ub  + v["ub"]
        lb       = lb  + v["lb"]
        colnames = colnames + v["name"]
        types    = types + v["type"]
    #####################################################################
    # Extract constraints
    rows = []; senses = []; rhs = [];
    for c in vonstraints:
        rows   = rows   + c["lin_expr"]
        senses = senses + c["senses"]
        rhs    = rhs    + c["rhs"]
    #####################################################################
    # Creating problem
    prob = cplex.Cplex()
    
    #Disable logging
    if not verbose:
        prob.set_log_stream(None)
        prob.set_error_stream(None)
        prob.set_warning_stream(None)
        prob.set_results_stream(None)
    
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