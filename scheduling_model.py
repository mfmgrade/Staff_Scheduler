from ortools.sat.python import cp_model

def create_schedule(employees, min_employees_per_shift, max_employees_per_shift):
    # Create the model.
    model = cp_model.CpModel()

    # Initialize the schedule with shifts instead of days
    shifts = [f'{day}-{shift}' for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'] for shift in ['Morning', 'Afternoon']]
    num_shifts = len(shifts)
    num_employees = len(employees)
    
    # Create shift variables.
    # shifts[(n, m)]: employee 'n' works shift 'm'.
    shifts_var = {}
    for n in range(num_employees):
        for m in range(num_shifts):
            shifts_var[(n, m)] = model.NewBoolVar(f'shifts_n{n}m{m}')
    
    # Each shift is assigned to at least min_employees_per_shift employees.
    for m in range(num_shifts):
        model.Add(sum(shifts_var[(n, m)] for n in range(num_employees)) >= min_employees_per_shift)

    # Each employee works at most their max_shifts_per_employee shifts.
    for n, (employee_id, (restrictions, max_shifts_per_employee)) in enumerate(employees.items()):
        model.Add(sum(shifts_var[(n, m)] for m in range(num_shifts)) <= max_shifts_per_employee)
        
        # Each employee works only shifts that are not in their restrictions.
        for m, shift in enumerate(shifts):
            if shift in restrictions:
                model.Add(shifts_var[(n, m)] == 0)
    
    # Create the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)

    # Create the resulting schedule.
    schedule = {shift: [] for shift in shifts}
    shifts_per_employee = {employee_id: 0 for employee_id in employees}
    for n, (employee_id, _) in enumerate(employees.items()):
        for m, shift in enumerate(shifts):
            if solver.Value(shifts_var[(n, m)]):
                schedule[shift].append(employee_id)
                shifts_per_employee[employee_id] += 1

    return schedule, shifts_per_employee