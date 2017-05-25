
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