from Bio.SeqUtils import gc_fraction
from read_stats.logging_config import setup_logger

# logging.basicConfig(filename='log/unmapped_reads.log', level=logging.INFO)
logger = setup_logger(__name__, log_file="unmapped_reads.log")

def compute_stats(read):
    if read.is_unmapped:
        logger.info("Unmapped read: %s", read.query_name)
        return

    try:
        frag_length = compute_fragment_length(read)
        base_qualities = compute_base_qualities(read)
        avg_base_quality = compute_avg_quality(base_qualities)
        read_seq = read.query_sequence or ""
        gc_content = gc_fraction(read_seq) if read_seq else 0
        num_mismatches = read.get_tag("NM") if read.has_tag("NM") else None
        
        return {
            "ReadID": read.query_name,
            "FragmentLength": frag_length,
            "AvgBaseQuality": avg_base_quality,
            "GCContent": gc_content,
            "NumMismatches": num_mismatches,
            "Chromosome": read.reference_name,
            "Start": read.reference_start,
            "End": read.reference_end
        }
    except Exception as e:
        logger.error("Error processing read %s: %s", read.query_name, e)
        raise

def compute_fragment_length(read):
    return abs(read.template_length)

def compute_base_qualities(read):
    return read.query_qualities or []

def compute_avg_quality(read_base_qualities):
    return sum(read_base_qualities) / len(read_base_qualities) if read_base_qualities else 0
