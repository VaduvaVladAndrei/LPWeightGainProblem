from pulp import *


def create_variables(foods):
    variables = []
    for day in range(1, 8):
        this_day = []
        for food in foods:
            this_day.append(LpVariable(f"{food}_d{day}", 0, None, LpInteger))
        variables.append(this_day)

    return variables


def build_min_function(variables):
    s = 0
    for day in range(0, 7):
        s += 10 * variables[day][0] + 1 * variables[day][1] + 1.5 * variables[day][2] + 5 * variables[day][3] + 4 * \
             variables[day][4] + 1 * variables[day][5] + 0.5 * variables[day][6] + 1 * variables[day][7]
    return s


def define_problem():
    model = LpProblem("DietProblem", LpMinimize)
    foods = ["Carne de vita", "Carne de curcan", "Ceapa", "Morcov", "Ardei gras", "Orez", "Cartofi prajiti", "Fasole"]

    variables = create_variables(foods)
    model += build_min_function(variables)

    # Constraint creation
    # Constraints for nutritional values
    for day in range(0, 7):
        model += 220 * variables[day][0] + 159 * variables[day][1] + 25 * variables[day][2] + 41 * variables[day][
            3] + 31 * variables[day][4] + 130 * variables[day][5] + 319 * variables[day][6] + 127 * variables[day][
                     7] >= 2500, f"Calories_d{day}"
        model += 24 * variables[day][0] + 2 * variables[day][1] + 2.7 * variables[day][2] + 29 * variables[day][3] + 4 * \
                 variables[day][4] + 9 * variables[day][5] + 1 * variables[day][6] + 1 * variables[day][
                     7] >= 90, f"Protein_d{day}"
        model += 0 * variables[day][0] + 10 * variables[day][1] + 29 * variables[day][2] + 0 * variables[day][3] + 38 * \
                 variables[day][4] + 24 * variables[day][5] + 10 * variables[day][6] + 6 * variables[day][
                     7] >= 273, f"Carbohydrates_d{day}"
        model += 55 * variables[day][0] + 10 * variables[day][1] + 4 * variables[day][2] + 56 * variables[day][3] + 70 * \
                 variables[day][4] + 171 * variables[day][5] + 600 * variables[day][6] + 200 * variables[day][
                     7] >= 115, f"Vitamins_d{day}"

    # Quantity constraints
    for day in range(0, 7):
        for food in range(0, len(foods)):
            model += variables[day][food] <= 4

    # Minimum quantity constraints
    for food in range(0, len(foods)):
        s = 0
        for day in range(0, 7):
            s += variables[day][food]
        model += s >=2

    # Precedence constraints
    for day in range(1, 7):
        for food in range(0, len(foods)):
            model += variables[day][food] + variables[day - 1][food] <= 5

    model.solve()
    for v in model.variables():
        print(v.name, "=", v.varValue)


def main():
    define_problem()


if __name__ == "__main__":
    main()
