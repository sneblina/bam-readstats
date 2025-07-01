import pandas as pd
import dash
from .logging_config import setup_logger
from dash import html, dash_table

logger = setup_logger(__name__)

def write_tsv(df:pd.DataFrame, output_path):
    # if not df:
    #     logger.warning("No stats to write to TSV.")
    #     return
    df["AvgBaseQuality"] = df["AvgBaseQuality"].map(lambda x: f"{x:.2f}")
    df["GCContent"] = df["GCContent"].map(lambda x: f"{x:.2f}")
    df["NumMismatches"] = df["NumMismatches"].apply(lambda x: int(x) if pd.notnull(x) else "")

    df.to_csv(output_path, sep="\t", index=False,
            columns=["ReadID", "FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"])

def create_dash_app(stats):
    """Create Dash app showing stats and overlap summary."""
    df = pd.DataFrame(stats)
    df["FragmentLength"] = df["FragmentLength"].astype(int)
    df["Overlap"] = df["Overlap"].astype(int)
    overlap_count = df["Overlap"].sum()
    app = dash.Dash(__name__)
    app.layout = html.Div([
        html.H1("Read Statistics Report"),
        html.P(f"Total Mapped Reads: {len(stats)}"),
        html.P(f"Overlapping Reads (with BED regions): {overlap_count}"),
        dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            page_size=20,
            filter_action="native",
            sort_action="native",
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        ),
    ])
    return app



def write_html(stats, overlap_count, output_path):
    html = f"""<html><head><title>Read Stats</title></head><body>
    <h1>Read Statistics</h1>
    <p>Total Mapped Reads: {len(stats)}</p>
    <p>Overlapping Reads: {overlap_count}</p>
    <table border='1'>
    <tr>
        <th>ReadID</th>
        <th>FragmentLength</th>
        <th>AvgBaseQuality</th>
        <th>GCContent</th>
        <th>NumMismatches</th>
    </tr>
    """

    for s in stats:
        if s is not None:
            # Format floats to 2 decimals, handle None gracefully
            avg_qual = f"{s['AvgBaseQuality']:.2f}" if s['AvgBaseQuality'] is not None else ""
            gc_cont = f"{s['GCContent']:.2f}" if s['GCContent'] is not None else ""
            num_mismatches = s['NumMismatches'] if s['NumMismatches'] is not None else ""

            html += f"<tr><td>{s['ReadID']}</td><td>{s['FragmentLength']}</td><td>{avg_qual}</td><td>{gc_cont}</td><td>{num_mismatches}</td></tr>\n"
        else:
            html += "<tr><td colspan='5'>No data available</td></tr>\n"

    # Close table and body tags OUTSIDE the loop!
    html += "</table></body></html>"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)