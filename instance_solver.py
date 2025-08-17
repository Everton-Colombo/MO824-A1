import pyomo
from pyomo.opt import SolverFactory
import pyomo.environ as pyo
from pyomo.environ import ConcreteModel, Var, RangeSet

from typing import Tuple, List, Dict

def create_model_from_instance(qbf_instance: Tuple[int, List[List[int]], List[List[float]]]) -> pyo.Model:
    n, sets, A = qbf_instance
    
    model = pyo.ConcreteModel()

    ## Vars:
    model.I = RangeSet(n)
    model.x = Var(model.I, domain=pyo.Binary)

    model.IJs = pyo.Set(dimen=2, initialize=[(i, j) for i in model.I for j in model.I if i <= j]) # Only take elements on the diagonal and above
    model.y = Var(model.IJs, domain=pyo.Binary)

    ## Objective:
    def objective_rule(model):
        return sum(A[i-1][j-1] * model.y[i, j] for (i, j) in model.IJs)

    model.obj = pyo.Objective(rule=objective_rule, sense=pyo.maximize)

    ## Constraints:

    # Linearization contraints (definition of y_{i, j})
    model.y_constraints = pyo.ConstraintList()
    for (i, j) in model.IJs:
        model.y_constraints.add(expr=model.y[i, j] <= model.x[i])                   # 1
        model.y_constraints.add(expr=model.y[i, j] <= model.x[j])                   # 2
        model.y_constraints.add(expr=model.y[i, j] >= model.x[i] + model.x[j] - 1)  # 3
        

    # Set-cover contraints:
    model.set_cover_contraints = pyo.ConstraintList()
    universe = set.union(*sets)
    for element in universe:
        # Get all indexes from the sets that contain element:
        containing_sets_idx: List[int] = []
        for i, curr_set in enumerate(sets):
            if element in curr_set:
                containing_sets_idx.append(i)
        
        model.set_cover_contraints.add(expr=sum(model.x[i+1] for i in containing_sets_idx) >= 1)
        
    return model

def solve_qbf_model(model: pyo.Model, time_limit_secs: int=10*60, tee=True) -> Dict:
    opt = SolverFactory('gurobi_persistent') # Model persists in memory after solve, intead of being discarded. Allows for accessing properties after solve.
    opt.set_instance(model)
    model_results = opt.solve(
        tee=tee,
        options={
            "TimeLimit": time_limit_secs
        }
    )
    
    solcount = opt.get_model_attr('SolCount')
    solver_runtime_sec = opt.get_model_attr('Runtime')  
    best_bound = opt.get_model_attr('ObjBound')                         # dual (best bound)
    incumbent = opt.get_model_attr('ObjVal') if solcount > 0 else None  # primal (incumbent)
    mip_gap = opt.get_model_attr('MIPGap')

    
    abs_gap = abs(incumbent - best_bound) if incumbent is not None else None

    
    output_results = {
        "objective": pyo.value(model.obj),
        "variables": [pyo.value(model.x[i]) for i in model.I],
        "primal": incumbent,
        "dual": best_bound,
        "relative_gap": mip_gap,
        "absolute_gap": abs_gap,
        "solver_runtime_sec": solver_runtime_sec,
        "model_results": model_results,
    }
    
    return output_results

def present_results(results_dict, inst):
    n, sets, A = inst
    vars_ = results_dict.get("variables", [])
    obj = results_dict.get("objective")
    rel_gap = results_dict.get("relative_gap")
    abs_gap = results_dict.get("absolute_gap")
    run = results_dict.get("solver_runtime_sec")

    chosen = [i + 1 for i, v in enumerate(vars_) if v >= 0.5]  # 1-based
    universe_all = set.union(*sets) if sets else set()
    covered = set().union(*(sets[i - 1] for i in chosen)) if chosen else set()
    coverage_pct = (len(covered) / len(universe_all) * 100) if universe_all else 0.0

    print("Solution summary")
    print(f"- Objective value: {obj}")
    if rel_gap is not None:
        print(f"- Gap: relative={rel_gap:.2%}, absolute={abs_gap}")
    if run is not None:
        print(f"- Solver Runtime: {run:.2f}")
    print(f"- Selected sets ({len(chosen)}/{n}): {chosen}")
    print(f"- Coverage: {len(covered)}/{len(universe_all)} elements ({coverage_pct:.1f}%)")
    print("- Variables:")
    for i, v in enumerate(vars_, start=1):
        print(f"  x[{i}] = {v:.0f}")
    