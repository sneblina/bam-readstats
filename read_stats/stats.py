import logging
from Bio.SeqUtils import gc_fraction

# Setup logging
logging.basicConfig(filename='unmapped_reads.log', level=logging.INFO)

def compute_stats(read):
    if read.is_unmapped:
        logging.info("Unmapped read: %s", read.query_name)

    try:
        frag_length = compute_frag_length(read)
        base_qualities = compute_base_qualities(read)
        avg_quality = compute_avg_quality(base_qualities)
        read_seq = read.query_sequence or ""
        gc_content = gc_fraction(read_seq) if read_seq else 0
        num_mismatches = read.get_tag("NM") if read.has_tag("NM") else None

        return {
            "ReadID": read.query_name,
            "FragmentLength": frag_length,
            "AvgBaseQuality": avg_quality,
            "GCContent": gc_content,
            "NumMismatches": num_mismatches,
            "chrom": read.reference_name,
            "start": read.reference_start,
            "end": read.reference_end
        }
    except Exception as e:
        logging.error("Error processing read %s: %s", read.query_name, e)
        raise

def compute_frag_length(read):
    return abs(read.template_length)

def compute_base_qualities(read):
    return read.query_qualities or []

def compute_avg_quality(base_qualities):
    return sum(base_qualities) / len(base_qualities) if base_qualities else 0

