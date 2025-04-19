import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from pandas.plotting import table

def _highlight_mismatches(df1: pd.DataFrame, df2: pd.DataFrame, max_rows=10):
    """
    Compare two dataframes and return two styled dataframes that highlight mismatched cells in red.
    """
    df1, df2 = df1.copy(), df2.copy()
    min_rows = min(len(df1), len(df2), max_rows)
    min_cols = min(len(df1.columns), len(df2.columns))

    df1 = df1.iloc[:min_rows, :min_cols]
    df2 = df2.iloc[:min_rows, :min_cols]

    highlight_df1 = df1.astype(str)
    highlight_df2 = df2.astype(str)

    for r in range(min_rows):
        for c in df1.columns[:min_cols]:
            val1 = str(df1.loc[r, c]).strip()
            val2 = str(df2.loc[r, c]).strip()
            if val1 != val2:
                highlight_df1.loc[r, c] = f"**{val1}**"
                highlight_df2.loc[r, c] = f"**{val2}**"

    return highlight_df1, highlight_df2

def _style_and_plot(df: pd.DataFrame, title: str, ax):
    ax.axis("off")
    ax.set_title(title, fontsize=12)
    
    cell_text = df.values
    rows, cols = df.shape
    color_matrix = []

    for r in range(rows):
        row_colors = []
        for c in range(cols):
            if "**" in str(cell_text[r][c]):
                row_colors.append(to_rgba("lightcoral", 0.6))
                cell_text[r][c] = cell_text[r][c].replace("**", "")
            else:
                row_colors.append(to_rgba("white", 0.0))
        color_matrix.append(row_colors)

    tab = table(ax, df, loc="center", cellLoc='left', colWidths=[0.1]*cols)
    
    for (r, c), cell in tab.get_celld().items():
        if r == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor("#f2f2f2")
        elif r > 0 and c < cols:
            cell.set_facecolor(color_matrix[r-1][c])
    
    tab.scale(1, 1.2)

def generate_proof_image(before_df: pd.DataFrame, after_df: pd.DataFrame, filename: str, output_folder="proofs"):
    os.makedirs(output_folder, exist_ok=True)

    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    fig.subplots_adjust(hspace=0.5)

    df1_highlighted, df2_highlighted = _highlight_mismatches(before_df, after_df)

    _style_and_plot(df1_highlighted, "Before File (highlighted)", ax[0])
    _style_and_plot(df2_highlighted, "After File (highlighted)", ax[1])

    proof_path = os.path.join(output_folder, f"{filename}_proof.png")
    plt.savefig(proof_path, bbox_inches="tight", dpi=200)
    plt.close()
    return proof_path
