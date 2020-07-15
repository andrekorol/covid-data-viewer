from operator import sub

import numpy as np
import pandas as pd

from data import get_data

# Antes de começar, é preciso baixar os dados no formato CSV do Our World In Data
csv_data = get_data()
df = pd.read_csv(csv_data)  # abre os dados em um pandas DataFrame

# O processo será repetido até o usuário solicitar para sair do programa
answer = "y"
while answer.lower() != "n":
    # Escolhe dois dias para calcular a porcentagem da diferença entre
    # os números de casos e depois gerar os gráficos
    first_day = input("Entre a data do primeiro dia no formato YYYY-MM-DD: ")
    second_day = input("Entre a data do segundo dia no formato YYYY-MM-DD: ")

    # Filtra os dados para cada dia no DataFrame
    first_day_data = df.loc[df["date"] == first_day]
    second_day_data = df.loc[df["date"] == second_day]

    # Informa o número de casos no mundo todo para cada dia,
    # assim como a porcentagem da diferença entre um dia e outro
    first_day_cases = first_day_data.loc[first_day_data["location"] == "World"][
        "total_cases"
    ].values[0]

    second_day_cases = second_day_data.loc[second_day_data["location"] == "World"][
        "total_cases"
    ].values[0]

    print(f"Número de casos em {first_day}: {int(first_day_cases)}")
    print(f"Número de casos em {second_day}: {int(second_day_cases)}")

    percentage_difference = round(
        (second_day_cases - first_day_cases)
        / min([first_day_cases, second_day_cases])
        * 100,
        2,
    )

    print(
        f"{first_day} --> {second_day}: {'+' if percentage_difference > 0 else ''}{percentage_difference}%"
    )

    # Ordena os dias para facilitar na computação
    [first_day, second_day] = sorted([first_day, second_day])

    # Filtra os dados novamente
    first_day_data = df.loc[df["date"] == first_day]
    second_day_data = df.loc[df["date"] == second_day]

    # Passa os pandas DataFrames para Numpy ndarrays
    np_second_day_cases = second_day_data["total_cases"].to_numpy()
    np_first_day_cases = first_day_data["total_cases"].to_numpy()

    # Redimensiona o array para cobrir os casos em que ha mais paises reportados
    # no segundo dia do que no primeiro
    nan_fill_shape = tuple(
        map(sub, np_second_day_cases.shape, np_first_day_cases.shape)
    )
    np_first_day_cases = np.hstack(
        [
            np_first_day_cases[:-1],
            np.full(nan_fill_shape, np.nan),
            np_first_day_cases[-1],
        ]
    )

    # Calcula as porcentagens das diferenças
    differences = (np_second_day_cases - np_first_day_cases) / np_first_day_cases * 100

    # Grava em um novo arquivo as informações selecionadas anteriormente
    # (país e porcentagem)
    with open(f"pct-diff-{first_day}-{second_day}.csv", "w") as fin:
        fin.write("pais,pct_diff\n")
        for pais, pct_diff in zip(second_day_data["location"], differences):
            fin.write(f"{pais},{pct_diff}\n")

    answer = input("Deseja continuar? [Y/n] ")
