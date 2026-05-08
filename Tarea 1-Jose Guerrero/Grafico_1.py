import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

df = pd.read_csv("nba_advanced_2025.csv")

df = df[df["Player"] != "League Average"]
df = df[df["TS%"].notna()]

df = df[~df["Team"].str.contains("TM", na=False)]

posiciones = ["PG", "SG", "SF", "PF", "C"]
df = df[df["Pos"].isin(posiciones) & (df["G"] >= 20)]
df["TS%"] = pd.to_numeric(df["TS%"], errors="coerce")
df = df.dropna(subset=["TS%"])
colores = {
    "PG": "#378ADD",
    "SG": "#1D9E75",
    "SF": "#D85A30",
    "PF": "#7F77DD",
    "C":  "#BA7517",
}
nombres = {
    "PG": "Base (PG)",
    "SG": "Escolta (SG)",
    "SF": "Alero (SF)",
    "PF": "Ala-Pívot (PF)",
    "C":  "Pívot (C)",
}

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#FAFAFA")
ax.set_facecolor("#FAFAFA")

datos_por_pos = [df[df["Pos"] == p]["TS%"].values for p in posiciones]

partes = ax.violinplot(
    datos_por_pos,
    positions=range(len(posiciones)),
    showmedians=True,
    showextrema=True,
    widths=0.6,
)

for i, pc in enumerate(partes["bodies"]):
    c = colores[posiciones[i]]
    pc.set_facecolor(c)
    pc.set_alpha(0.5)
    pc.set_edgecolor(c)

partes["cmedians"].set_color("white")
partes["cmedians"].set_linewidth(2)
partes["cmins"].set_color("#888")
partes["cmaxes"].set_color("#888")
partes["cbars"].set_color("#888")

for i, pos in enumerate(posiciones):
    vals = df[df["Pos"] == pos]["TS%"].values
    jitter = np.random.uniform(-0.12, 0.12, size=len(vals))
    ax.scatter(
        [i] * len(vals) + jitter,
        vals,
        color=colores[pos],
        alpha=0.4,
        s=18,
        zorder=3,
    )

ax.set_xticks(range(len(posiciones)))
ax.set_xticklabels([nombres[p] for p in posiciones], fontsize=11)
ax.set_ylabel("True Shooting %", fontsize=12)
ax.set_xlabel("Posicion", fontsize=12)
ax.set_title(
    "Distribucion de True Shooting % por posicion — NBA 2024-25",
    fontsize=13,
    fontweight="bold",
    pad=14,
)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.grid(axis="y", linestyle="--", alpha=0.4)
ax.spines[["top", "right"]].set_visible(False)

leyenda = [
    mpatches.Patch(facecolor=colores[p], alpha=0.6, label=nombres[p])
    for p in posiciones
]
ax.legend(handles=leyenda, loc="upper left", fontsize=9, framealpha=0.5)

ax.text(
    0.99, 0.01,
    "Fuente: Basketball-Reference.com",
    transform=ax.transAxes,
    fontsize=8,
    color="#888",
    ha="right",
    va="bottom",
)

plt.tight_layout()
plt.savefig("ts_posicion.png", dpi=150, bbox_inches="tight")