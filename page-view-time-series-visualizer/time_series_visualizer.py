import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Charger les données
file_path = Path(__file__).parent / "fcc-forum-pageviews.csv"

df = pd.read_csv(
    file_path,
    index_col="date",
    parse_dates=True
)

# Nettoyer les données : enlever les 2,5 % les plus bas et les 2,5 % les plus hauts
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    fig, ax = plt.subplots(figsize=(20, 5))

    ax.plot(df.index, df["value"], color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig(Path(__file__).parent / "line_plot.png")

    return fig


def draw_bar_plot():
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_bar["month_name"] = df_bar.index.month_name()

    df_bar = (
        df_bar.groupby(["year", "month", "month_name"])["value"]
        .mean()
        .reset_index()
    )

    month_order = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    df_bar = df_bar.pivot(
        index="year",
        columns="month_name",
        values="value"
    )

    df_bar = df_bar.reindex(columns=month_order)

    ax = df_bar.plot(kind="bar", figsize=(12, 8))
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig = ax.get_figure()
    fig.savefig(Path(__file__).parent / "bar_plot.png")

    return fig


def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month

    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    df_box = df_box.sort_values("month_num")

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig(Path(__file__).parent / "box_plot.png")

    return fig