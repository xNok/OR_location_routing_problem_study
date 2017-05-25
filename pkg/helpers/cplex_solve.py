
import cplex

def cplex_solve_extract_variables(variables):
    obj = [];ub = [];lb = [];colnames = [];types = [];
    for v in variables:
        if "loop" in v:
            ## evaluation of the loop
            v["coef"] = eval("[" + v["coef"] + v["loop"] + "]")
            v["ub"]   = eval("[" + v["ub"] + v["loop"] + "]")
            v["lb"]   = eval("[" + v["lb"] + v["loop"] + "]")
            v["name"] = eval("[" + v["name"] + v["name"] + "]")
            v["type"] = eval("[" + v["type"] + v["loop"] + "]")
            
        # Concatenation of variables attributes
        obj      = obj + v["coef"]
        ub       = ub  + v["ub"]
        lb       = lb  + v["lb"]
        colnames = colnames + v["name"]
        types    = types + v["type"]
        
    return obj, ub, lb, colnames, types

def cplex_solve_extract_constraints(constraints):
    rows = []; senses = []; rhs = [];
    for c in constraints:
        if "loop" in c:
            c["lin_expr"] = eval("[" + c["lin_expr"] + c["loop"] + "]")
            c["senses"]   = eval("[" + c["senses"] + c["loop"] + "]")
            c["rhs"]      = eval("[" + c["rhs"] + c["loop"] + "]")
            
        # Concatenation of variables attributes    
        rows   = rows   + c["lin_expr"]
        senses = senses + c["senses"]
        rhs    = rhs    + c["rhs"]
        
    return rows, senses, rhs

def cplex_solve(variables,constraints, minimize=True, path=None, verbose=False):
    
    #####################################################################
    # Extract variables
    obj, ub, lb, colnames, types = cplex_solve_extract_variables(variables)
    #####################################################################
    # Extract constraints
    rows, senses, rhs = cplex_solve_extract_constraints(constraints)
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