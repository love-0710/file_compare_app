import os
import pandas as pd
from jinja2 import Template

def generate_csv_report(result_df: pd.DataFrame, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    result_df.to_csv(output_path, index=False)

def generate_html_report(result_df: pd.DataFrame, output_path: str, proof_paths: dict = None):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if proof_paths:
        result_df["Proof"] = result_df.apply(
            lambda row: f"<img src='{proof_paths.get(row['Filename'], '')}' width='300'>" 
            if row['Filename'] in proof_paths else "N/A", axis=1)

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SmartComparePro - Comparison Report</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .highlight { background-color: #ffcccc; }
        </style>
    </head>
    <body>
        <h1>SmartComparePro - Comparison Report</h1>
        <p>Generated Report</p>
        {{ table | safe }}
    </body>
    </html>
    """

    template = Template(html_template)
    rendered_html = template.render(table=result_df.to_html(escape=False, index=False))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
