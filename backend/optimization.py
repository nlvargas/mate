from collections import defaultdict
import pulp


def comb(x_list, y_list):
    return ((x, y) for x in x_list for y in y_list)


def prefered_groups(student, G):
    gr = []
    for preference in student["preferences"]:
        groups = list(filter(lambda g: "Grupo {} - ".format(preference) in g, G))
        gr = gr + groups
    return gr


def run(params):
    # -------------------- Params --------------------
    attr_bounds = params["attributes"]
    preferences = list(params["preferences"].keys())
    groups_number = params["groups_number"]
    lower_number = params["lower_number"]
    upper_number = params["upper_number"]
    attr = params['student_attr']  # 1 si alumno i tiene el atributo r
    preferences_bounds = params["preferences"]
    students = params["students"]
    # -------------------- Sets --------------------
    G = ["Grupo {} - (N{})".format(p, n) for p in preferences for n in range(1, groups_number + 1)]
    I = list(students.keys())  # alumnos
    G_t = defaultdict(list)  # grupos asociados al tema t
    not_answered = [students[student].id for student in filter(lambda i: not students[i].answered, students)]
  
    for g in G:
        for p in preferences:
            if "Grupo {} - ".format(p) in g:
                G_t[p].append(g)

    priority = {s: defaultdict(lambda: 100) for s in students}
    for s in students.values():
        for i, preference in enumerate(s["preferences"]):
            groups_prefered = list(filter(lambda g: "Grupo {} - ".format(s["preferences"][preference]) in g, G))
            for g in groups_prefered:
                priority[s["id"]][g] = i + 1
    # big_index = ((i, j, a, g) for i in I for j in I for a in A for g in G)
    # -------------------- Model --------------------
    model = pulp.LpProblem("Assign", pulp.LpMinimize)
    # -------------------- Vars --------------------
    y = pulp.LpVariable.dicts("y", comb(I, G), cat='Binary')
    w = pulp.LpVariable.dicts("w", G, lowBound=0, upBound=1, cat='Continuous')
    z = pulp.LpVariable.dicts("z", I, lowBound=0, cat='Continuous')
    z_max = pulp.LpVariable("z_max", cat='Continuous')
    f = pulp.LpVariable.dicts("f", I, cat='Binary')
    Q = pulp.LpVariable.dicts("Q", comb(G, A), cat='Continuous')  # N de alumnos con la caracteristica r en el grupo g
    P = pulp.LpVariable.dicts("P", comb(G, A), cat='Binary')   # 1 si no hay alumnos con la caracteristica r en el grupo g
    F = pulp.LpVariable.dicts("F", comb(G, A), cat='Continuous') 
    M = pulp.LpVariable.dicts("M", G, lowBound=0, cat='Continuous')
    M_max = pulp.LpVariable("M_max", cat='Continuous')
    #O = pulp.LpVariable.dicts("O", big_index, cat='Binary')
    # -------------------- Constraints --------------------

    for g in G:
        model += (pulp.lpSum([y[i, g] for i in not_answered]) <= 1 + M[g],
              "No puede haber mas de un alumno que no contesta en el grupo {}".format(g))
        model += (M_max >= M[g],
                "Definicion M_max para cada grupo {}".format(g))

    for preference in preferences_bounds:
        pref_groups = list(filter(lambda g: "Grupo {} - ".format(preference) in g, G))
        model += (pulp.lpSum([w[g] for g in pref_groups]) >= int(preferences_bounds[preference]["min"]),
                "Numero minimo de grupos armados con la preferencia '{}'".format(preference))

        model += (pulp.lpSum([w[g] for g in pref_groups]) <= int(preferences_bounds[preference]["max"]),
                "Numero max de grupos armados con la preferencia '{}'".format(preference))

    for i in I:
        model += (z[i] == pulp.lpSum([y[i, g] * int(priority[i][g]) for g in G]),
                  "Prioridad obtenida por el alumno {}".format(i))

        model += (z_max >= z[i],
                  "Definicion z_max para cada el alumno {}".format(i))

        model += (pulp.lpSum([y[i, g] for g in G]) == 1,
                  "Alumno {} es asignado a un grupo".format(i))

        model += (1 - pulp.lpSum([y[i, g] for g in prefered_groups(students[i], G)]) <= f[i],
                  "f vale 1 si el alumno {} no queda en ninguna preferencia".format(i))

        for g in G:
            model += (w[g] >= y[i, g],
                      "El grupo {} esta activo si hay al menos un alumno {} asignado a ese grupo".format(g, i))

            #for j in I:
            #    if i != j:
            #        for r in A:
            #            if r not in attr_bounds:
            #                model += (attr[i][r] * y[i, g] + attr[j][r] <= O[i, j, r, g] + 1,
            #                          "Activar variable de diversidad {}_{}_{}_{}".format(i, j, g, r))

    model += (pulp.lpSum([w[g] for g in G]) == groups_number,
              "Numero total de grupos")
   
    for g in G:
        model += (pulp.lpSum([y[i, g] for i in not_answered]) <= 1,
              "No puede haber mas de un alumno que no contesta en el grupo {}".format(g))
    for g in G:
        model += (lower_number * w[g] <= pulp.lpSum([y[(i, g)] for i in I]),
                  "Numero minimo de alumnos en grupo {}".format(g))

        model += (pulp.lpSum([y[i, g] for i in I]) <= upper_number * w[g],
                  "Numero maximo de alumnos en grupo {}".format(g))

        for a in attr_bounds:
            for r in attr_bounds[a]:
                if not attr_bounds[a][r]["solo"]:
                    model += (int(attr_bounds[a][r]["min"]) * w[g] <= pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Numero minimo de alumnos con atributo '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (int(attr_bounds[a][r]["max"]) * w[g] >= pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Numero maximo de alumnos con atributo '{}', opcion '{}' en el grupo {}".format(a, r, g))
                else:
                    model += (attr_bounds[a][r]["min"] * (w[g] - P[g, r]) <= Q[g, r],
                            "Numero minimo de alumnos con atributo aux '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (attr_bounds[a][r]["max"] * (1 - P[g, r]) >= Q[g, r],
                            "Numero maximo de alumnos con atributo aux '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (Q[g, r] == pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Act. Q '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (F[g, r] >= Q[g, r] - attr_bounds[a][r]["min"],
                            "Act. F '{}', opcion '{}' en el grupo {}".format(a, r, g))

    # -------------------- Objective --------------------
    model += pulp.lpSum(
        [1000 * z_max] +
        [1000000 * f[i] for i in I] +
        [100 * M_max]
        #[100 * O[i, j, a, g] for i in I for j in I for a in A for g in G]
    )
    model.solve()
    pulp.LpStatus[model.status]

    results = []
    for g in G:
        students = [i for i in I if y[i, g].varValue != 0]
        if students:
            results.append({"group": g, "students": students})
    factible = True if model.status != -1 else False
    return {"results": results, "factible": factible}

def run_modules(params):
    # -------------------- Params --------------------
    attr_bounds = params["attributes"]
    preferences = list(params["preferences"].keys())
    groups_number = params["groups_number"]
    lower_number = params["lower_number"]
    upper_number = params["upper_number"]
    attr = params['student_attr']  # 1 si alumno i tiene el atributo r
    preferences_bounds = params["preferences"]
    students = params["students"]
    cap = params["capacity"]
    modules = params["modules"]
    not_answered = [students[student]["id"] for student in filter(lambda i: not students[i]["answered"], students)]
        # -------------------- Sets --------------------
    A = params["A"]  # Lista de opciones de todos los atributos
    D = [d for d in modules]
    G = ["Grupo {} - {} (N{})".format(p, d, n)  # grupos posibles
            for p in preferences for d in modules for n in range(1, groups_number + 1)]
    I = list(students.keys())  # alumnos
    G_t = defaultdict(list)  # grupos asociados al tema t
    G_d = defaultdict(list)  # grupos asociados al dia/seccion d
    for g in G:
        for p in preferences:
            if "Grupo {} - ".format(p) in g:
                G_t[p].append(g)
        for d in D:
            if " - {} (N".format(d) in g:
                G_d[d].append(g)

    priority = {s: defaultdict(lambda: 100) for s in students}
    for s in students.values():
        for i, preference in enumerate(s["preferences"]):
            groups_prefered = list(filter(lambda g: "Grupo {} - ".format(s["preferences"][preference]) in g, G))
            for g in groups_prefered:
                priority[s["id"]][g] = i + 1
    # big_index = ((i, j, a, g) for i in I for j in I for a in A for g in G)
    # -------------------- Model --------------------
    model = pulp.LpProblem("Assign", pulp.LpMinimize)
    # -------------------- Vars --------------------
    y = pulp.LpVariable.dicts("y", comb(I, G), cat='Binary')
    w = pulp.LpVariable.dicts("w", G, lowBound=0, upBound=1, cat='Continuous')
    z = pulp.LpVariable.dicts("z", I, lowBound=0, cat='Continuous')
    z_max = pulp.LpVariable("z_max", cat='Continuous')
    f = pulp.LpVariable.dicts("f", I, cat='Binary')
    Q = pulp.LpVariable.dicts("Q", comb(G, A), cat='Continuous')  # N de alumnos con la caracteristica r en el grupo g
    P = pulp.LpVariable.dicts("P", comb(G, A), cat='Binary')   # 1 si no hay alumnos con la caracteristica r en el grupo g
    F = pulp.LpVariable.dicts("F", comb(G, A), cat='Continuous') 
    M = pulp.LpVariable.dicts("M", G, lowBound=0, cat='Continuous')
    M_max = pulp.LpVariable("M_max", cat='Continuous')
    
    #O = pulp.LpVariable.dicts("O", big_index, cat='Binary')
    # -------------------- Constraints --------------------
    #print("PRIORITY")
    #print(priority)

    for g in G:
        model += (pulp.lpSum([y[i, g] for i in not_answered]) <= 1 + M[g],
              "No puede haber mas de un alumno que no contesta en el grupo {}".format(g))
        model += (M_max >= M[g],
                "Definicion M_max para cada grupo {}".format(g))

    for preference in preferences_bounds:
        pref_groups = list(filter(lambda g: "Grupo {} - ".format(preference) in g, G))
        model += (pulp.lpSum([w[g] for g in pref_groups]) >= int(preferences_bounds[preference]["min"]),
                "Numero minimo de grupos armados con la preferencia '{}'".format(preference))

        model += (pulp.lpSum([w[g] for g in pref_groups]) <= int(preferences_bounds[preference]["max"]),
                "Numero max de grupos armados con la preferencia '{}'".format(preference))

    for i in I:
        model += (z[i] == pulp.lpSum([y[i, g] * int(priority[i][g]) for g in G]),
                "Prioridad obtenida por el alumno {}".format(i))

        model += (z_max >= z[i],
                "Definicion z_max para cada el alumno {}".format(i))

        model += (pulp.lpSum([y[i, g] for g in G]) == 1,
                "Alumno {} es asignado a un grupo".format(i))

        model += (1 - pulp.lpSum([y[i, g] for g in prefered_groups(students[i], G)]) <= f[i],
                "f vale 1 si el alumno {} no queda en ninguna preferencia".format(i))

        for g in G:
            model += (w[g] >= y[i, g],
                    "El grupo {} esta activo si hay al menos un alumno {} asignado a ese grupo".format(g, i))

            #for j in I:
            #    if i != j:
            #        for r in A:
            #            if r not in attr_bounds:
            #                model += (attr[i][r] * y[i, g] + attr[j][r] <= O[i, j, r, g] + 1,
            #                          "Activar variable de diversidad {}_{}_{}_{}".format(i, j, g, r))

    model += (pulp.lpSum([w[g] for g in G]) == groups_number,
            "Numero total de grupos")

    for g in G:
        model += (lower_number * w[g] <= pulp.lpSum([y[i, g] for i in I]),
                "Numero minimo de alumnos en grupo {}".format(g))

        model += (pulp.lpSum([y[i, g] for i in I]) <= upper_number * w[g],
                "Numero maximo de alumnos en grupo {}".format(g))

        for a in attr_bounds:
            for r in attr_bounds[a]:
                if not attr_bounds[a][r]["solo"]:
                    model += (int(attr_bounds[a][r]["min"]) * w[g] <= pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Numero minimo de alumnos con atributo '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (int(attr_bounds[a][r]["max"]) * w[g] >= pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Numero maximo de alumnos con atributo '{}', opcion '{}' en el grupo {}".format(a, r, g))
                else:
                    model += (attr_bounds[a][r]["min"] * (w[g] - P[g, r]) <= Q[g, r],
                            "Numero minimo de alumnos con atributo aux '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (attr_bounds[a][r]["max"] * (1 - P[g, r]) >= Q[g, r],
                            "Numero maximo de alumnos con atributo aux '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (Q[g, r] == pulp.lpSum([y[i, g] * attr[i][r] for i in I]),
                            "Act. Q '{}', opcion '{}' en el grupo {}".format(a, r, g))

                    model += (F[g, r] >= Q[g, r] - attr_bounds[a][r]["min"],
                            "Act. F '{}', opcion '{}' en el grupo {}".format(a, r, g))
    
    for d in D:
        model += (pulp.lpSum([y[i, g] for i in I for g in G_d[d]]) <= cap[d],
                            "Capacidad maxima '{}'".format(d))
        for i in I:
            model += (pulp.lpSum([y[i, g] for g in G_d[d]]) <= int(students[i]["a"][d]),
                            "Disponibilidad {} de {}".format(d, i))

    # -------------------- Objective --------------------
    model += pulp.lpSum(
        [1000 * z_max] +
        [1000000 * f[i] for i in I] +
        [100 * M_max]
        #[100 * O[i, j, a, g] for i in I for j in I for a in A for g in G]
    )
    model.solve()
    pulp.LpStatus[model.status]
    results = []
    for g in G:
        students = [i for i in I if y[i, g].varValue != 0]
        if students:
            results.append({"group": ' '.join(g.split(" ")[:-1]), "students": students})
            # results.append({"group": g, "students": students})
    factible = True if model.status != -1 else False

    return {"results": results, "factible": factible}