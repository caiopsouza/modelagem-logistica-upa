import sys
from itertools import product
from pulp import LpVariable, const, LpProblem, LpMinimize, lpSum, LpStatus


def dist_squared(a: (int, int), b: (int, int)) -> int:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def upa(distritos: [int, int], dist_max_distrito_upa: [int], dist_min_entre_upas: int):
    dist_max_distrito_upa = sorted(dist_max_distrito_upa)

    # Lista de índices dos distritos
    range_distritos = list(range(0, len(distritos)))

    # Variáveis do problema. Cada variável terá um valor binário indicando se a UPA deve ser instalada no distrito.
    variables = {k: LpVariable(f"x{k}", cat=const.LpBinary) for k in range_distritos}

    # O objetivo é minimizar o número de UPAs instaladas
    problem = LpProblem("UPA", LpMinimize)
    problem += lpSum(variables.items())

    # Distância máxima entre um distrito e a próxima UPA
    dist_max_distrito_upa_squared = [d * d for d in dist_max_distrito_upa]
    amount_required = 1
    for dist_max_squared in dist_max_distrito_upa_squared:
        print('params', amount_required, dist_max_squared)

        for distrito in range_distritos:
            restricoes_distancia = []

            for vizinho in range_distritos:
                distancia_squared = dist_squared(distritos[distrito], distritos[vizinho])
                dentro_da_area = distancia_squared <= dist_max_squared

                restricoes_distancia.append(variables[vizinho] * dentro_da_area)

            problem += lpSum(restricoes_distancia) >= amount_required
            amount_required += 1

    # Distância mínima entre UPAs
    dist_min_entre_upas_squared = dist_min_entre_upas * dist_min_entre_upas
    for (distrito, vizinho) in product(range_distritos, range_distritos):
        if distrito == vizinho:
            continue

        distancia_squared = dist_squared(distritos[distrito], distritos[vizinho])

        if distancia_squared <= dist_min_entre_upas_squared:
            problem += variables[distrito] + variables[vizinho] <= 1

    # Resolve
    print(problem)
    problem.solve()
    print(LpStatus[problem.status])


if __name__ == '__main__':
    distritos_localidades = [
        (64, 74),
        (40, 9),
        (59, 5),
        (43, 6),
        (69, 51),
        (47, 15),
        (2, 87),
        (1, 61),
        (5, 41),
        (4, 49),
        (25, 82),
        (6, 46),
        (93, 95),
        (98, 3),
        (88, 65),
        (48, 28),
        (47, 18),
        (52, 75),
        (94, 84),
        (54, 83),
        (48, 80),
        (62, 87),
        (9, 76),
        (39, 47),
        (99, 0),
        (83, 21),
        (35, 13),
        (6, 32),
        (31, 59),
        (48, 48),
        (63, 25),
        (76, 47),
        (64, 42),
        (72, 66),
        (23, 49),
        (19, 15),
        (1, 63),
        (60, 60),
        (85, 73),
        (17, 50),
        (76, 47),
        (92, 68),
        (75, 62),
        (58, 9),
        (32, 42),
        (22, 58),
        (41, 36),
        (94, 18),
        (23, 46),
        (50, 96),
        (32, 25),
        (56, 64),
        (27, 31),
        (45, 9),
        (79, 41),
        (55, 69),
        (7, 57),
        (88, 31),
        (7, 40),
        (42, 2),
    ]
    dist_max_distrito_upa = [10, 15]
    dist_min_entre_upas = 3
    upa(distritos_localidades, dist_max_distrito_upa, dist_min_entre_upas)
