def write_html(stats, overlap_count, output_path):
    html = f"""<html><head><title>Read Stats</title></head><body>
    <h1>Read Statistics</h1>
    <p>Total Reads: {len(stats)}</p>
    <p>Overlapping Reads: {overlap_count}</p>
    <table border='1'>
    <tr><th>ReadName</th><th>FragmentLength</th><th>AvgBaseQuality</th><th>GCContent</th><th>NumMismatches</th></tr>
    """

    for s in stats:
        # html += f"<tr><td>{s['fragment_length']}</td><td>{s['avg_base_quality']:.2f}</td><td>{s['gc_content']}</td><td>{s['num_mismatches']}</td></tr>\n"
        if s is not None:
            html += f"<tr><td>{s['read_id']}</td><td>{s['fragment_length']}</td><td>{s['avg_base_quality']:.2f}</td><td>{s['gc_content']}</td><td>{s['num_mismatches']}</td></tr>\n"
        else:
            # Optionally log or handle missing data
            html += "<tr><td colspan='4'>No data available</td></tr>\n"
        
        html += "</table></body></html>"

    with open(output_path, "w") as f:
        f.write(html)
