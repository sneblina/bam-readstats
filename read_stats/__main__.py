# __main__.py

from read_stats.cli import parse_args   
from read_stats.stats import compute_stats
from read_stats.io_utils import read_bam, check_overlap
from read_stats.report import write_tsv, create_dash_app

def main():
    args = parse_args()
    bam = read_bam(args.bam)
    bed = args.bed
    output_path = args.output

    stats = []
    
    for read in bam.fetch():
        read_stats = compute_stats(read)
        if not read_stats:
            continue
        stats.append(read_stats)
    
    output_df = check_overlap(stats, bed)

    # write_html(stats, overlap_count, output_path + '/output.html') #input this path
    write_tsv(output_df, output_path + '/output.tsv') #input this path
    app = create_dash_app(output_df)
    app.run(debug=False, host="localhost", port=8050)

if __name__ == "__main__":
    main()