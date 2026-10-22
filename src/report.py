"""Production des éléments du rapport à partir de PostgreSQL.

- docs/livraison/figures/<langue>/*.png : graphiques en français (fr) et en anglais (en) ;
- docs/livraison/resultats.md           : résultats de chaque requête SQL, régénérés à chaque exécution.

Exécution seule :  python -m src.report
"""

import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from src import config  # noqa: E402
from src.load import connect  # noqa: E402

logger = logging.getLogger(__name__)

DELIVERY_DIR = config.PROJECT_DIR / "docs" / "livraison"
FIGURES_DIR = DELIVERY_DIR / "figures"
LANGUAGES = ("fr", "en")

INK, INK_SECONDARY, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
SERIES = {"afr": "#2a78d6", "global": "#eb6834"}            # palette validée (projet 0)
POOR, RICH = "#eb6834", "#2a78d6"
STATUS_COLORS = ["#1baf7a", "#2a78d6", "#eda100", "#e34948"]

LABELS = {
    "fr": {
        "decimal": ",", "percent": "{:.0f} %",
        "q1_title": "Q1 · Mortalité des moins de 5 ans, région africaine",
        "met": "cible déjà atteinte", "not_met": "cible non atteinte",
        "q1_x": "Décès pour 1 000 naissances vivantes", "target": "cible ODD 2030 : {:g}",
        "world": "monde : {:.0f}",
        "trend_title": "Mortalité des moins de 5 ans : région africaine et monde",
        "trend_y": "Décès pour 1 000 naissances vivantes", "afr": "Région africaine (OMS)", "global": "Monde",
        "q2_title": "Q2 · Trajectoire vers les cibles de 2030 (pays de la région africaine)",
        "q2_x": "Nombre de pays",
        "status": ["Cible déjà atteinte", "En bonne voie", "Progrès insuffisants", "Stagnation ou recul"],
        "short": {"MDG_0000000026": "Mortalité maternelle", "MDG_0000000007": "Moins de 5 ans",
                  "WHOSIS_000003": "Néonatale"},
        "q3_title": "Q3 · Mortalité des moins de 5 ans : 20 % les plus pauvres vs 20 % les plus riches",
        "q3_x": "Décès pour 1 000 naissances vivantes (estimations 2024)",
        "poor": "20 % les plus pauvres", "rich": "20 % les plus riches",
        "q4_title": "Q4 · Moyens du système de santé et mortalité des moins de 5 ans",
        "q4_y": "Mortalité < 5 ans (‰)", "rho": "ρ de Spearman = {:.2f}",
        "inputs": {"WHS4_100": "Couverture DTP3 (%)", "MDG_0000000025": "Accouchements assistés (%)",
                   "HWF_0001": "Médecins / 10 000 hab.", "GHED_CHE_pc_US_SHA2011": "Dépenses de santé / hab. (USD)"},
    },
    "en": {
        "decimal": ".", "percent": "{:.0f}%",
        "q1_title": "Q1 · Under-five mortality, African Region",
        "met": "target already met", "not_met": "target not met",
        "q1_x": "Deaths per 1,000 live births", "target": "2030 SDG target: {:g}",
        "world": "world: {:.0f}",
        "trend_title": "Under-five mortality: African Region and world",
        "trend_y": "Deaths per 1,000 live births", "afr": "African Region (WHO)", "global": "World",
        "q2_title": "Q2 · Trajectory towards the 2030 targets (African Region countries)",
        "q2_x": "Number of countries",
        "status": ["Target already met", "On track", "Insufficient progress", "Stagnation or decline"],
        "short": {"MDG_0000000026": "Maternal mortality", "MDG_0000000007": "Under-five",
                  "WHOSIS_000003": "Neonatal"},
        "q3_title": "Q3 · Under-five mortality: poorest 20% vs richest 20%",
        "q3_x": "Deaths per 1,000 live births (2024 estimates)",
        "poor": "Poorest 20%", "rich": "Richest 20%",
        "q4_title": "Q4 · Health system inputs and under-five mortality",
        "q4_y": "Under-5 mortality (‰)", "rho": "Spearman ρ = {:.2f}",
        "inputs": {"WHS4_100": "DTP3 coverage (%)", "MDG_0000000025": "Skilled birth attendance (%)",
                   "HWF_0001": "Doctors per 10,000", "GHED_CHE_pc_US_SHA2011": "Health spending per capita (USD)"},
    },
}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_SECONDARY, "axes.titlecolor": INK,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.color": INK_SECONDARY, "ytick.color": INK_SECONDARY,
    "font.size": 9, "legend.frameon": False,
})


def query(connection, sql: str) -> pd.DataFrame:
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [column.name for column in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)


def _save(fig, folder: Path, name: str) -> None:
    fig.tight_layout()
    fig.savefig(folder / name, dpi=150)
    plt.close(fig)


def _number(value: float, text: dict, digits: int = 0) -> str:
    return f"{value:,.{digits}f}".replace(",", " " if text["decimal"] == "," else ",").replace(".", text["decimal"])


# --- Graphiques ----------------------------------------------------------------

def figure_q1(data: pd.DataFrame, world: float, text: dict, folder: Path) -> None:
    data = data.sort_values("value")
    fig, ax = plt.subplots(figsize=(8, 9.5))
    colors = [SERIES["afr"] if v > 25 else "#1baf7a" for v in data["value"]]
    ax.barh(data["location_name"], data["value"], color=colors, height=0.65)
    ax.axvline(25, color=INK, linewidth=1.2, linestyle="--")
    ax.annotate(text["target"].format(25), (25, len(data) - 0.5), xytext=(4, 0), textcoords="offset points",
                fontsize=8.5, color=INK, va="top")
    ax.axvline(world, color=SERIES["global"], linewidth=1.2)
    ax.annotate(text["world"].format(world), (world, 0), xytext=(4, 0), textcoords="offset points",
                fontsize=8.5, color=INK_SECONDARY)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.grid(axis="y", visible=False)
    ax.margins(y=0.01)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=SERIES["afr"], label=text["not_met"]), Patch(color="#1baf7a", label=text["met"])],
              loc="lower right")
    ax.set_xlabel(text["q1_x"])
    ax.set_title(text["q1_title"])
    _save(fig, folder, "q1_mortalite_moins_5_ans.png")


def figure_trend(data: pd.DataFrame, text: dict, folder: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 3.6))
    for key in ("afr", "global"):
        series = data[data["serie"] == key].sort_values("year")
        ax.plot(series["year"], series["value"], color=SERIES[key], linewidth=2, label=text[key])
        ax.fill_between(series["year"], series["value_low"], series["value_high"], color=SERIES[key], alpha=0.12)
    ax.axhline(25, color=INK, linewidth=1, linestyle="--")
    ax.annotate(text["target"].format(25), (data["year"].min(), 25), xytext=(2, 4), textcoords="offset points",
                fontsize=8.5, color=INK)
    ax.set_ylabel(text["trend_y"])
    ax.set_title(text["trend_title"])
    ax.legend(loc="upper right")
    _save(fig, folder, "q1_tendance_region_monde.png")


def figure_q2(summary: pd.DataFrame, text: dict, folder: Path) -> None:
    columns = ["deja_atteinte", "en_bonne_voie", "progres_insuffisants", "stagnation_ou_recul"]
    summary = summary.set_index("indicateur")
    fig, ax = plt.subplots(figsize=(8, 2.8))
    labels = [text["short"][code] for code in summary.index]
    left = [0] * len(summary)
    for column, label, color in zip(columns, text["status"], STATUS_COLORS):
        values = summary[column].astype(int).tolist()
        bars = ax.barh(labels, values, left=left, color=color, label=label, height=0.55,
                       edgecolor=SURFACE, linewidth=2)
        for bar, value in zip(bars, values):
            if value >= 2:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, str(value),
                        ha="center", va="center", fontsize=8.5, color="white", fontweight="bold")
        left = [a + b for a, b in zip(left, values)]
    ax.grid(axis="y", visible=False)
    ax.invert_yaxis()
    ax.set_xlabel(text["q2_x"])
    ax.set_title(text["q2_title"])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=4, fontsize=8)
    _save(fig, folder, "q2_trajectoires_2030.png")


def figure_q3(data: pd.DataFrame, text: dict, folder: Path) -> None:
    data = data.sort_values("ratio_pauvres_riches")
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.28 * len(data) + 1)))
    names = list(data["pays"])
    ax.hlines(names, data["mortalite_q5_plus_riches"], data["mortalite_q1_plus_pauvres"], color=GRID, linewidth=3)
    ax.scatter(data["mortalite_q5_plus_riches"], names, color=RICH, s=40, zorder=3, label=text["rich"],
               edgecolor=SURFACE, linewidth=1.5)
    ax.scatter(data["mortalite_q1_plus_pauvres"], names, color=POOR, s=40, zorder=3, label=text["poor"],
               edgecolor=SURFACE, linewidth=1.5)
    for name, poor, ratio in zip(names, data["mortalite_q1_plus_pauvres"], data["ratio_pauvres_riches"]):
        ax.annotate(f"×{_number(float(ratio), text, 1)}", (poor, name), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=7.5, color=INK_SECONDARY)
    ax.tick_params(axis="y", labelsize=7.5)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel(text["q3_x"])
    ax.set_title(text["q3_title"])
    ax.legend(loc="lower right")
    _save(fig, folder, "q3_inegalites_richesse.png")


def figure_q4(data: pd.DataFrame, correlations: pd.DataFrame, text: dict, folder: Path) -> None:
    codes = list(text["inputs"])
    fig, axes = plt.subplots(2, 2, figsize=(8, 6), sharey=True)
    for ax, code in zip(axes.flat, codes):
        subset = data[data["indicator_code"] == code]
        ax.scatter(subset["moyen"], subset["u5mr"], s=22, color=SERIES["afr"], alpha=0.75, edgecolor=SURFACE)
        if code == "GHED_CHE_pc_US_SHA2011":
            ax.set_xscale("log")   # dépenses de 20 à 700 USD : l'échelle log évite d'écraser les petits pays
            ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([20, 50, 100, 200, 500]))
            ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}"))
            ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        rho = correlations.loc[correlations["indicateur"] == code, "correlation_spearman"]
        ax.set_title(text["rho"].format(float(rho.iloc[0])) if len(rho) else "", fontsize=9, fontweight="normal")
        ax.set_xlabel(text["inputs"][code])
    for ax in axes[:, 0]:
        ax.set_ylabel(text["q4_y"])
    fig.suptitle(text["q4_title"], x=0.01, ha="left", fontsize=12, fontweight="bold")
    _save(fig, folder, "q4_moyens_resultats.png")


# --- Résultats SQL -----------------------------------------------------------------

def _markdown_table(frame: pd.DataFrame) -> str:
    def cell(value) -> str:
        return "" if value is None or (isinstance(value, float) and pd.isna(value)) else str(value)
    header = "| " + " | ".join(frame.columns) + " |"
    separator = "|" + "---|" * len(frame.columns)
    rows = ["| " + " | ".join(cell(v) for v in row) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, separator, *rows])


def write_results(connection) -> None:
    run = query(connection, "SELECT max(raw_batch) AS lot FROM ops.pipeline_run WHERE status = 'success'")
    sections = ["# Résultats des requêtes SQL", "",
                f"> Fichier **généré automatiquement** par `python -m src.report` (lot brut du {run['lot'][0]}).",
                "> Ne pas modifier à la main : relancer le pipeline pour le régénérer."]
    for path in sorted(config.SQL_DIR.glob("*.sql")):
        if path.name[:2] in ("00", "01"):
            continue
        sections += ["", f"## `{path.name}`", "", _markdown_table(query(connection, path.read_text(encoding="utf-8")))]
    (DELIVERY_DIR / "resultats.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def build_report() -> None:
    with connect() as connection:
        sql = lambda name: (config.SQL_DIR / name).read_text(encoding="utf-8")  # noqa: E731
        u5 = query(connection, """
            SELECT location_name, value::float AS value FROM core.v_latest
            WHERE indicator_code = 'MDG_0000000007' AND location_type = 'COUNTRY' AND who_region = 'AFR'""")
        world = float(query(connection, """
            SELECT value::float AS value FROM core.v_latest
            WHERE indicator_code = 'MDG_0000000007' AND location_type = 'GLOBAL'""")["value"][0])
        trend = query(connection, """
            SELECT CASE WHEN location_type = 'GLOBAL' THEN 'global' ELSE 'afr' END AS serie, year,
                   value::float AS value, value_low::float AS value_low, value_high::float AS value_high
            FROM core.v_national
            WHERE indicator_code = 'MDG_0000000007' AND year >= 1990
              AND ((location_type = 'REGION' AND location_code = 'AFR') OR location_type = 'GLOBAL')""")
        summary = query(connection, sql("q2b_synthese_rythme.sql"))
        inequality = query(connection, sql("q3_inegalites_richesse.sql"))
        correlations = query(connection, sql("q4_moyens_resultats.sql"))
        inputs = query(connection, """
            WITH d AS (SELECT * FROM core.v_latest WHERE location_type = 'COUNTRY' AND who_region = 'AFR' AND year >= 2015)
            SELECT m.indicator_code, m.value::float AS moyen, u.value::float AS u5mr
            FROM d AS m JOIN d AS u ON u.location_code = m.location_code AND u.indicator_code = 'MDG_0000000007'
            WHERE m.role = 'moyen'""")

        for language in LANGUAGES:
            folder = FIGURES_DIR / language
            folder.mkdir(parents=True, exist_ok=True)
            text = LABELS[language]
            figure_q1(u5, world, text, folder)
            figure_trend(trend, text, folder)
            figure_q2(summary, text, folder)
            figure_q3(inequality, text, folder)
            figure_q4(inputs, correlations, text, folder)
        write_results(connection)
    logger.info("Graphiques (%s) et résultats écrits dans %s", ", ".join(LANGUAGES), DELIVERY_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    build_report()
