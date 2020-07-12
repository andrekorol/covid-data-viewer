import pandas as pd

if __name__ == "__main__":
    from data import get_data

    csv_data = get_data()
    df = pd.read_csv(csv_data)
    print(df)
