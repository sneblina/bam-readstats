import csv
import pysam
from pybedtools import BedTool

def read_bam(bam_path):
    return pysam.AlignmentFile(bam_path, "rb")

def load_bed(bed_path):
    return BedTool(bed_path)

def check_overlap(read_stat, bed_regions):
    from pybedtools import BedTool
    tmp_bed = BedTool(f"{read_stat['chrom']}\t{read_stat['start']}\t{read_stat['end']}", from_string=True)
    return tmp_bed.intersect(bed_regions, u=True).count() > 0

def write_tsv(stats, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(stats)
        # writer.writerow(["FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches"])
        # for s in stats:
        #     writer.writerow([
        #         s["fragment_length"],
        #         f"{s['avg_base_quality']:.2f}",
        #         f"{s['gc_content']:.2f}",
        #         s["num_mismatches"]
        #     ])
