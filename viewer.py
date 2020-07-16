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
    first_day_df = df.loc[df["date"] == first_day]
    second_day_df = df.loc[df["date"] == second_day]

    # Encontra o dia com o menor numero de lugares com dados reportados
    least_locations_df = sorted(
        [first_day_df, second_day_df], key=lambda day_df: day_df["location"].shape
    )[0]

    # Grava em um novo arquivo as informações selecionadas (país e porcentagem)
    with open(f"pct-diff-{first_day}-{second_day}.csv", "w") as fin:
        fin.write("pais,pct_diff\n")
        # Calcula as porcentagens das diferenças para cada lugar
        for location in least_locations_df["location"]:
            first_day_cases = first_day_df.loc[first_day_df["location"] == location][
                "total_cases"
            ].values[0]
            second_day_cases = second_day_df.loc[second_day_df["location"] == location][
                "total_cases"
            ].values[0]
            pct_diff = round(
                (second_day_cases - first_day_cases)
                / min([first_day_cases, second_day_cases])
                * 100,
                2,
            )
            fin.write(f"{location},{pct_diff}\n")
            # Informa o número de casos no mundo todo para cada dia, assim
            # como a porcentagem da diferença entre um dia e outro
            if location == "World":
                print(f"Número de casos em {first_day}: {int(first_day_cases)}")
                print(f"Número de casos em {second_day}: {int(second_day_cases)}")
                print(
                    f"{first_day} --> {second_day}: {'+' if pct_diff > 0 else ''}{pct_diff}%"
                )

    answer = input("Deseja continuar? [Y/n] ")
