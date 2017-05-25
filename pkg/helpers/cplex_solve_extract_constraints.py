
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