import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import parallel_coordinates

# Cargar datos
csv_file = 'nba_advanced_2025.csv'
df = pd.read_csv(csv_file)

# Normalizar la columna de posición para agrupar por la posición principal
position_regex = r'(PG|SG|SF|PF|C)'
df['Position'] = df['Pos'].astype(str).str.extract(position_regex, expand=False)

# Filtrar solo jugadores con al menos 40 partidos jugados
filtered = df[df['G'] >= 40].copy()

# Si hay jugadores con varias filas (2TM + equipos), quedarnos con la fila de mayor G
filtered = filtered.sort_values(['Player', 'G'], ascending=[True, False])
filtered = filtered.drop_duplicates(subset='Player', keep='first')

# Métricas avanzadas para visualizar
metrics = ['PER', 'TS%', 'BPM', 'VORP', 'WS']

# Asegurarnos de que las métricas sean numéricas
for metric in metrics:
    filtered[metric] = pd.to_numeric(filtered[metric], errors='coerce')

# Elegir los mejores jugadores por WS para mantener el gráfico claro
selected = filtered.sort_values('WS', ascending=False).head(50).copy()

# Normalizar métricas para que compartan la misma escala
normalized = selected[metrics].apply(lambda x: (x - x.min()) / (x.max() - x.min()))
plot_df = pd.concat([selected[['Player', 'Position']].reset_index(drop=True), normalized.reset_index(drop=True)], axis=1)

# Definir colores consistentes para cada posición
position_order = ['PG', 'SG', 'SF', 'PF', 'C']
palette = sns.color_palette('tab10', n_colors=len(position_order))
position_colors = {pos: palette[i] for i, pos in enumerate(position_order)}

# Asegurar que solo se grafiquen posiciones válidas
plot_df = plot_df[plot_df['Position'].isin(position_order)].copy()

# Plot
sns.set_theme(style='whitegrid')
plt.figure(figsize=(16, 10))
ax = plt.gca()
parallel_coordinates(
    plot_df,
    class_column='Position',
    cols=metrics,
    color=[position_colors[pos] for pos in position_order],
    alpha=0.65,
    linewidth=1.4,
    ax=ax
)

# Añadir etiquetas de jugador al final de cada línea
for line, player in zip(ax.lines, plot_df['Player']):
    xdata = line.get_xdata()
    ydata = line.get_ydata()
    ax.text(
        xdata[-1] + 0.4,
        ydata[-1],
        player,
        fontsize=7,
        color=line.get_color(),
        alpha=0.9,
        ha='left',
        va='center',
        clip_on=False
    )

x_last = len(metrics) - 1
ax.set_xlim(-0.5, x_last + 1.7)
plt.title('Rendimiento avanzado de jugadores NBA 2024-25 (top 50 por WS)', fontsize=18, weight='bold')
plt.xlabel('Métricas avanzadas normalizadas', fontsize=14)
plt.ylabel('Valor relativo (0.0 - 1.0)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

legend = plt.legend(title='Posición', fontsize=12, title_fontsize=13, loc='upper right', frameon=True)
legend.get_frame().set_edgecolor('black')
legend.get_frame().set_alpha(0.85)

plt.text(
    0.99,
    0.03,
    'Fuente: Basketball-Reference.com',
    ha='right',
    va='bottom',
    transform=plt.gca().transAxes,
    fontsize=11,
    color='gray'
)

plt.tight_layout()
plt.savefig('grafico_grupal_ia.png', dpi=150)
