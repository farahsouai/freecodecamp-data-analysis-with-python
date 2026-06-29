import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
from pathlib import Path


def draw_plot():
    # Charger les données
    file_path = Path(__file__).parent / "epa-sea-level.csv"
    df = pd.read_csv(file_path)

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(10, 6))

    # Nuage de points
    ax.scatter(
        df["Year"],
        df["CSIRO Adjusted Sea Level"]
    )

    # Première droite de régression : toutes les années
    result_all = linregress(
        df["Year"],
        df["CSIRO Adjusted Sea Level"]
    )

    years_all = range(1880, 2051)
    sea_levels_all = [
        result_all.slope * year + result_all.intercept
        for year in years_all
    ]

    ax.plot(years_all, sea_levels_all, "r")

    # Deuxième droite : données depuis 2000
    df_recent = df[df["Year"] >= 2000]

    result_recent = linregress(
        df_recent["Year"],
        df_recent["CSIRO Adjusted Sea Level"]
    )

    years_recent = range(2000, 2051)
    sea_levels_recent = [
        result_recent.slope * year + result_recent.intercept
        for year in years_recent
    ]

    ax.plot(years_recent, sea_levels_recent, "g")

    # Titres et labels demandés
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level (inches)")
    ax.set_title("Rise in Sea Level")

    # Sauvegarder l'image dans le dossier du projet
    fig.savefig(Path(__file__).parent / "sea_level_plot.png")

    return ax