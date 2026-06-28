import pandas as pd
from pathlib import Path


def calculate_demographic_data(print_data=True):
    file_path = Path(__file__).parent / "adult.data.csv"
    df = pd.read_csv(file_path)

    # Nombre de personnes par race
    race_count = df["race"].value_counts()

    # Âge moyen des hommes
    average_age_men = round(
        df[df["sex"] == "Male"]["age"].mean(),
        1
    )

    # Pourcentage de personnes titulaires d'un bachelor
    percentage_bachelors = round(
        (df["education"] == "Bachelors").mean() * 100,
        1
    )

    # Études supérieures
    higher_education = df["education"].isin(
        ["Bachelors", "Masters", "Doctorate"]
    )

    # Pourcentage avec études supérieures gagnant >50K
    higher_education_rich = round(
        (df[higher_education]["salary"] == ">50K").mean() * 100,
        1
    )

    # Pourcentage sans études supérieures gagnant >50K
    lower_education_rich = round(
        (df[~higher_education]["salary"] == ">50K").mean() * 100,
        1
    )

    # Nombre minimum d'heures travaillées
    min_work_hours = df["hours-per-week"].min()

    # Personnes travaillant le minimum d'heures
    min_workers = df[df["hours-per-week"] == min_work_hours]

    # Pourcentage de ces personnes gagnant >50K
    rich_percentage = round(
        (min_workers["salary"] == ">50K").mean() * 100,
        1
    )

    # Pourcentage de personnes gagnant >50K par pays
    country_income = (
        df[df["salary"] == ">50K"]
        .groupby("native-country")
        .size()
        / df.groupby("native-country").size()
        * 100
    )

    highest_earning_country = country_income.idxmax()
    highest_earning_country_percentage = round(
        country_income.max(),
        1
    )

    # Profession la plus fréquente en Inde parmi les personnes gagnant >50K
    top_IN_occupation = (
        df[
            (df["native-country"] == "India")
            & (df["salary"] == ">50K")
        ]["occupation"]
        .value_counts()
        .idxmax()
    )

    if print_data:
        print("Nombre de personnes par race :\n", race_count)
        print("Âge moyen des hommes :", average_age_men)
        print("Pourcentage de bachelors :", percentage_bachelors)
        print("Pourcentage études supérieures >50K :", higher_education_rich)
        print("Pourcentage sans études supérieures >50K :", lower_education_rich)
        print("Minimum d'heures travaillées :", min_work_hours)
        print("Pourcentage minimum-heures >50K :", rich_percentage)
        print("Pays avec le plus haut pourcentage >50K :", highest_earning_country)
        print("Pourcentage :", highest_earning_country_percentage)
        print("Profession la plus fréquente en Inde >50K :", top_IN_occupation)

    return {
        "race_count": race_count,
        "average_age_men": average_age_men,
        "percentage_bachelors": percentage_bachelors,
        "higher_education_rich": higher_education_rich,
        "lower_education_rich": lower_education_rich,
        "min_work_hours": min_work_hours,
        "rich_percentage": rich_percentage,
        "highest_earning_country": highest_earning_country,
        "highest_earning_country_percentage": highest_earning_country_percentage,
        "top_IN_occupation": top_IN_occupation
    }