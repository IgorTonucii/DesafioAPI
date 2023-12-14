from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine("sqlite:///:memory:")


def criar_tabela():
    df = pd.read_csv(
        r"c:\Users\Igor\Downloads\movielist.csv", #mudar arquivo
        delimiter=";",
    )
    df.to_sql("dados_filmes", engine)


def calcular_intervalos():
    query = "SELECT * FROM dados_filmes WHERE winner = 'yes' ORDER BY year"
    df_vitorias = pd.read_sql_query(query, engine)

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
    criar_tabela()
    df_vitorias = calcular_intervalos()

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
