import httpx


def get_data():
    csv_data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    local_data_file = "owid-covid-data.csv"
    with open(local_data_file, "wb") as fin:
        with httpx.stream("GET", csv_data_url) as resp:
            for data in resp.iter_bytes():
                fin.write(data)

    return local_data_file
