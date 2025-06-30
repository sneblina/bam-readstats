import csv
from pysam import AlignmentFile
from pybedtools import BedTool

# TODO: Introduce error handling # pylint: disable=fixme


def read_bam(bam_path):
    return AlignmentFile(bam_path, "rb")

def load_bed(bed_path):
    return BedTool(bed_path)

def check_overlap(read_stat, bed_regions):
    tmp_bed = BedTool(f"{read_stat['chrom']}\t{read_stat['start']}\t{read_stat['end']}", from_string=True)
    return tmp_bed.intersect(bed_regions, u=True).count() > 0

def write_tsv(stats, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["ReadID", "FragmentLength", "AvgBaseQuality", "GCContent", "NumMismatches"])
        for s in stats:
            writer.writerow([
                s["read_id"],
                s["fragment_length"],
                f"{s['avg_base_quality']:.2f}",
                f"{s['gc_content']:.2f}",
                s["num_mismatches"]
            ])
