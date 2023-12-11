from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)


def calcular_intervalos(df):
    df_vitorias = df[df["winner"] == "yes"].copy()
    df_vitorias["year"] = pd.to_numeric(df_vitorias["year"])

    df_vitorias = df_vitorias.sort_values(by="year")

    grouped = df_vitorias.groupby("producers")["year"].apply(list)

    intervalos = {"min": [], "max": []}

    for producer, years in grouped.items():
        if len(years) >= 2:
            diff_years = [years[i + 1] - years[i] for i in range(len(years) - 1)]
            menor_intervalo = min(diff_years)
            maior_intervalo = max(diff_years)

            min_index = diff_years.index(menor_intervalo)
            max_index = diff_years.index(maior_intervalo)

            menor = {
                "producer": producer,
                "previousWin": years[min_index],
                "followingWin": years[min_index + 1],
                "interval": menor_intervalo,
            }

            maior = {
                "producer": producer,
                "previousWin": years[max_index],
                "followingWin": years[max_index + 1],
                "interval": maior_intervalo,
            }

            if not intervalos["min"] or menor_intervalo < intervalos["min"][0].get(
                "interval", float("inf")
            ):
                intervalos["min"] = [menor]
            elif menor_intervalo == intervalos["min"][0]["interval"]:
                intervalos["min"].append(menor)

            if not intervalos["max"] or maior_intervalo > intervalos["max"][0].get(
                "interval", 0
            ):
                intervalos["max"] = [maior]
            elif maior_intervalo == intervalos["max"][0]["interval"]:
                intervalos["max"].append(maior)

    return intervalos


@app.route("/outputFinal")
def mostrar_intervalos():
    df = pd.read_csv(
        r"c:\Users\Igor\Downloads\movielist.csv",  # não esquecer de trocar o caminho do arquivo
        delimiter=";",
    )

    df_vitorias = calcular_intervalos(df)

    max_intervalo = df_vitorias["max"]
    min_intervalo = df_vitorias["min"]

    resultado = {
        "max": [
            {
                "producer": intervalo["producer"],
                "previousWin": int(intervalo["previousWin"]),
                "followingWin": int(intervalo["previousWin"] + intervalo["interval"]),
                "interval": int(intervalo["interval"]),
            }
            for intervalo in max_intervalo
        ],
        "min": [
            {
                "producer": intervalo["producer"],
                "previousWin": int(intervalo["previousWin"]),
                "followingWin": int(intervalo["previousWin"] + intervalo["interval"]),
                "interval": int(intervalo["interval"]),
            }
            for intervalo in min_intervalo
        ],
    }

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=True)
