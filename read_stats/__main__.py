# __main__.py

from read_stats.cli import parse_args
from read_stats.stats import compute_stats
from read_stats.file_reader import read_bam, read_bed
from read_stats.check_overlap import check_overlap
from read_stats.report import write_tsv, write_simple_html
from read_stats.logging_config import setup_logger

logger = setup_logger(__name__)

def main():
    args = parse_args()
    bam = read_bam(args.bam)
    bed = read_bed(args.bed) if args.bed else None
    output_path = args.output
    
    stats = []
    for read in bam.fetch():
        read_stats = compute_stats(read)
        if not read_stats:
            continue
        stats.append(read_stats)
    output_df = check_overlap(stats, bed)

    write_simple_html(output_df, output_path + '/output.html') #input this path
    write_tsv(output_df, output_path + '/output.tsv') #input this path

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("An error occurred: %s", e, exc_info=True)
        raise