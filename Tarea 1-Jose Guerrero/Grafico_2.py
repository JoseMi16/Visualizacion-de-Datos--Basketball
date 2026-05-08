import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np

df = pd.read_csv("nba_advanced_2025.csv")

df = df[df["Player"] != "League Average"]
df = df[~df["Team"].str.contains("TM", na=False)]

cols_num = ["PER", "USG%", "BPM", "G"]
for c in cols_num:
    df[c] = pd.to_numeric(df[c], errors="coerce")

posiciones = ["PG", "SG", "SF", "PF", "C"]
df = df[df["Pos"].isin(posiciones) & (df["G"] >= 40)].dropna(subset=cols_num)

colores = {
    "PG": "#378ADD",
    "SG": "#1D9E75",
    "SF": "#D85A30",
    "PF": "#7F77DD",
    "C":  "#BA7517",
}
nombres_pos = {
    "PG": "Base (PG)",
    "SG": "Escolta (SG)",
    "SF": "Alero (SF)",
    "PF": "Ala-Pívot (PF)",
    "C":  "Pívot (C)",
}

bpm_min = df["BPM"].min()
df["r"] = ((df["BPM"] - bpm_min + 1) ** 1.4) * 18

fig, ax = plt.subplots(figsize=(11, 7))
fig.patch.set_facecolor("#FFFFFF")
ax.set_facecolor("#FFFFFF")

for pos in posiciones:
    sub = df[df["Pos"] == pos]
    ax.scatter(
        sub["USG%"],
        sub["PER"],
        s=sub["r"],
        color=colores[pos],
        alpha=0.80,
        edgecolors=colores[pos],
        linewidths=0.5,
        label=nombres_pos[pos],
        zorder=3,
    )


overrides = {
    "Gilgeous-Alexander": "Shai G-A",
    "Antetokounmpo": "Giannis",
    "Haliburton": "Tyrese Haliburton",
    "Cunningham": "Cade Cunningham",
    "James": "LeBron James",
    "Towns": "K-A Towns",
}
for _, row in df.iterrows():
    apellido = row["Player"].split(" ")[-1]
    nombre = overrides.get(apellido, apellido)
    ax.annotate(
        nombre,
        (row["USG%"], row["PER"]),
        textcoords="offset points",
        xytext=(0, np.sqrt(row["r"]) / 2 + 4),
        fontsize=7.5,
        color="#222222",
        ha="center",
        va="bottom",
        path_effects=[pe.withStroke(linewidth=2.2, foreground="#FFFFFF")],
        zorder=5,
    )
ax.set_xlim(10, 38)
ax.set_ylim(14, 35)
ax.set_xticks(range(10, 39, 5))
ax.set_xticklabels([f"{v}%" for v in range(10, 39, 5)], fontsize=10)
ax.set_yticks(range(14, 36, 2))
ax.set_yticklabels([str(v) for v in range(14, 36, 2)], fontsize=10)
ax.set_xlabel("USG% (uso ofensivo)", fontsize=12)
ax.set_ylabel("PER (eficiencia)", fontsize=12)
ax.set_title(
    "PER vs Uso ofensivo (USG%) — NBA 2024-25\n(Box Plus/Minus)",
    fontsize=13,
    fontweight="bold",
    pad=14,
)

ax.grid(color="#DDDDDD", linestyle="-", linewidth=0.6, zorder=0)
ax.spines[["top", "right"]].set_visible(False)

ax.legend(loc="upper left", fontsize=9.5, framealpha=0.6, title="Posición", title_fontsize=9)

ax.text(
    0.99, 0.01,
    "Fuente: Basketball-Reference.com",
    transform=ax.transAxes,
    fontsize=8,
    color="#888888",
    ha="right",
    va="bottom",
)

plt.tight_layout()
plt.savefig("bubble_bpm.png", dpi=150, bbox_inches="tight")