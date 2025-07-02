import pandas as pd
import json
from read_stats.logging_config import setup_logger

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

def write_html(stats: pd.DataFrame, output_path: str):
        # Drop missing values just for plotting purposes
    stats_clean = stats[["AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"]].dropna()

    # Convert selected columns to a JSON dict for Plotly
    data_json = stats_clean.to_dict(orient="list")

    # HTML + Plotly Dashboard Template
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Read Stats Summary</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
            h1 {{
                text-align: center;
            }}
            .chart-container {{
                width: 48%;
                display: inline-block;
                vertical-align: top;
            }}
            .full-width {{
                width: 100%;
                margin-top: 30px;
            }}
        </style>
    </head>
    <body>
        <h1>Read Statistics Summary</h1>

        <div class="chart-container" id="avgBaseQuality"></div>
        <div class="chart-container" id="gcContent"></div>
        <div class="chart-container" id="numMismatches"></div>
        <div class="chart-container" id="overlapChart"></div>

        <script>
            const data = {json.dumps(data_json)};

            // AvgBaseQuality Histogram
            Plotly.newPlot('avgBaseQuality', [{{
                x: data.AvgBaseQuality,
                type: 'histogram',
                marker: {{ color: 'teal' }}
            }}], {{
                title: 'Average Base Quality Distribution',
                xaxis: {{ title: 'AvgBaseQuality' }},
                yaxis: {{ title: 'Count' }}
            }});

            // GCContent Histogram
            Plotly.newPlot('gcContent', [{{
                x: data.GCContent,
                type: 'histogram',
                marker: {{ color: 'purple' }}
            }}], {{
                title: 'GC Content Distribution',
                xaxis: {{ title: 'GCContent (%)' }},
                yaxis: {{ title: 'Count' }}
            }});

            // NumMismatches Bar Chart
            const mismatchCounts = {{
                x: Array.from(new Set(data.NumMismatches)).sort((a,b)=>a-b),
                y: []
            }};
            mismatchCounts.x.forEach(val => {{
                mismatchCounts.y.push(data.NumMismatches.filter(x => x === val).length);
            }});

            Plotly.newPlot('numMismatches', [{{
                x: mismatchCounts.x,
                y: mismatchCounts.y,
                type: 'bar',
                marker: {{ color: 'orange' }}
            }}], {{
                title: 'Number of Mismatches',
                xaxis: {{ title: 'NumMismatches' }},
                yaxis: {{ title: 'Count' }}
            }});

            // Overlap Pie Chart
            const overlapCounts = {{
                labels: ['No Overlap', 'Overlap'],
                values: [data.Overlap.filter(x => x == 0).length, data.Overlap.filter(x => x == 1).length]
            }};

            Plotly.newPlot('overlapChart', [{{
                labels: overlapCounts.labels,
                values: overlapCounts.values,
                type: 'pie'
            }}], {{
                title: 'Overlap Summary'
            }});
        </script>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

