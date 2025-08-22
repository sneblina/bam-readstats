import json
import os
import pandas as pd
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)

def write_tsv(df, output_path):
    if df.empty:
        logger.warning("No stats to write to TSV.")
        return
    # Use safe formatting for None values
    df["AvgBaseQuality"] = df["AvgBaseQuality"].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
    df["GCContent"] = df["GCContent"].map(lambda x: f"{x:.2f}" if pd.notnull(x) else "")
    df["NumMismatches"] = df["NumMismatches"].map(lambda x: int(x) if pd.notnull(x) else "")
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    df.to_csv(output_path, sep="\t", index=False,
            columns=["ReadID", "FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"])

def write_html(stats, output_path):
    # Drop missing values just for plotting purposes
    stats_clean = stats[["AvgBaseQuality", "GCContent", "NumMismatches", "Overlap"]]

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

def write_simple_html(stats, output_path):        
    overlap_count = stats["Overlap"].sum()
    avg_base_quality = stats["AvgBaseQuality"].mean()


    # Define bins and labels for fragment length
    bins = [0, 50] + [i for i in range(100, 655, 50)]
    fragment_labels = ["<50", "50-100"] + [f"{i}-{i+50}" for i in range(100, 650, 50)] + [">650"]

    # Assign bins
    cut_bins = bins + [float("inf")]
    stats["FragLenBin"] = pd.cut(
        stats["FragmentLength"],
        bins=cut_bins,
        labels=fragment_labels,
        right=True,
        include_lowest=True
    )

    bin_counts = stats["FragLenBin"].value_counts().reindex(fragment_labels, fill_value=0)
    total_reads = len(stats)
    fragment_table_rows = ""
    for label in fragment_labels:
        count = bin_counts[label]
        percent = (count / total_reads * 100) if total_reads > 0 else 0
        fragment_table_rows += f"<tr><td>{label}</td><td>{count}</td><td>{percent:.2f}</td></tr>\n"

    # GC content distribution table
    gc_bins = [0, 0.25, 0.5, 0.75, 1.0]
    gc_labels = ["0-0.25", "0.25-0.5", "0.5-0.75", "0.75-1.0"]
    stats["GCBin"] = pd.cut(
        stats["GCContent"],
        bins=gc_bins,
        labels=gc_labels,
        right=True,
        include_lowest=True
    )
    gc_bin_counts = stats["GCBin"].value_counts().reindex(gc_labels, fill_value=0)
    gc_table_rows = ""
    for label in gc_labels:
        bin_mask = stats["GCBin"] == label
        count = gc_bin_counts[label]
        percent = (count / total_reads * 100) if total_reads > 0 else 0
        avg_base_qual = stats.loc[bin_mask, "AvgBaseQuality"].mean()
        avg_base_qual_str = f"{avg_base_qual:.2f}" if count > 0 else "N/A"
        gc_table_rows += f"<tr><td>{label}</td><td>{count}</td><td>{percent:.2f}</td><td>{avg_base_qual_str}</td></tr>\n"

    # Mismatch statistics table
    mismatch_bins = list(range(0, 11)) + [float("inf")]
    mismatch_labels = [str(i) for i in range(0, 10)] + [">10"]
    stats["MismatchBin"] = pd.cut(
        stats["NumMismatches"],
        bins=mismatch_bins,
        labels=mismatch_labels,
        right=True,
        include_lowest=True
    )
    mismatch_bin_counts = stats["MismatchBin"].value_counts().reindex(mismatch_labels, fill_value=0)
    mismatch_table_rows = ""
    for label in mismatch_labels:
        count = mismatch_bin_counts[label]
        percent = (count / total_reads * 100) if total_reads > 0 else 0
        mismatch_table_rows += f"<tr><td>{label}</td><td>{count}</td><td>{percent:.2f}</td></tr>\n"

    html = f"""<html><head><title>Read Stats</title></head><body>
    <h1>Read Statistics Summary</h1>
    <ul>
        <li><strong>Total Mapped Reads:</strong> {total_reads}</li>
        <li><strong>Overlapping Reads:</strong> {overlap_count}</li>
        <li><strong>Average Base Quality:</strong> {avg_base_quality:.2f}</li>
    </ul>
    <h2>Fragment Length Distribution</h2>
    <table border="1" cellpadding="4" cellspacing="0">
        <tr>
            <th>Fragment Length Range (bp)</th>
            <th>Read Count</th>
            <th>% of Total</th>
        </tr>
        {fragment_table_rows}
    </table>
    <h2>GC Content Distribution</h2>
    <table border="1" cellpadding="4" cellspacing="0">
        <tr>
            <th>GC Content %</th>
            <th>Read Count</th>
            <th>% of Total</th>
            <th>Avg Base Quality</th>
        </tr>
        {gc_table_rows}
    </table>
    <h2>Mismatch Statistics</h2>
    <table border="1" cellpadding="4" cellspacing="0">
        <tr>
            <th>Num Mismatches</th>
            <th>Read Count</th>
            <th>% of Total</th>
        </tr>
        {mismatch_table_rows}
    </table>
    </body></html>"""

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


# def write_simple_html(stats, output_path):        
#     overlap_count = stats["Overlap"].sum()
#     html = f"""<html><head><title>Read Stats</title></head><body>
#     <h1>Read Statistics</h1>
#     <p>Total Mapped Reads: {len(stats)}</p>
#     <p>Overlapping Reads: {overlap_count}</p>
#     <table border='1'>
#     <tr>
#         <th>ReadID</th>
#         <th>FragmentLength</th>
#         <th>AvgBaseQuality</th>
#         <th>GCContent</th>
#         <th>NumMismatches</th>
#     </tr>
#     """

#     for _, s in stats.iterrows():
#         if s is not None:
#             # Format floats to 2 decimals, handle None gracefully
#             avg_qual = f"{s['AvgBaseQuality']:.2f}" if s['AvgBaseQuality'] is not None else ""
#             gc_cont = f"{s['GCContent']:.2f}" if s['GCContent'] is not None else ""
#             num_mismatches = s['NumMismatches'] if s['NumMismatches'] is not None else ""

#             html += f"<tr><td>{s['ReadID']}</td><td>{s['FragmentLength']}</td><td>{avg_qual}</td><td>{gc_cont}</td><td>{num_mismatches}</td></tr>\n"
#         else:
#             html += "<tr><td colspan='5'>No data available</td></tr>\n"

#     # Close table and body tags OUTSIDE the loop!
#     html += "</table></body></html>"
#     if not os.path.exists(os.path.dirname(output_path)):
#         os.makedirs(os.path.dirname(output_path))
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(html)