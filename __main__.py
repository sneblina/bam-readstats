# __main__.py

from .read_stats.cli import parse_args   
from .read_stats.stats import compute_stats
from .read_stats.io_utils import read_bam, load_bed, check_overlap, write_tsv
from .read_stats.report import write_html

def main():
    args = parse_args()
    bam = read_bam(args.bam)
    # bed = load_bed(args.bed)
    output_path = args.output

    stats = []
    overlap_count = 0

    for read in bam.fetch():
        s = compute_stats(read)
        # if not s:
        #     continue
        # if check_overlap(s, bed):
        #     overlap_count += 1
        stats.append(s)

    write_tsv(stats, output_path + '/output.tsv') #input this path
    write_html(stats, overlap_count, output_path + '/output.html') #input this path

if __name__ == "__main__":
    main()