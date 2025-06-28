# from Bio.SeqUtils import gc
import pysam

def compute_stats(read):
    if read.is_unmapped or read.is_secondary:
        return None
    frag_length = abs(read.template_length)
    base_qualities = read.query_qualities or []
    avg_quality = sum(base_qualities) / len(base_qualities) if base_qualities else 0
    read_seq = read.query_sequence or ""
    gc_content = 'to_be_filled'
    # gc_content = gc(read_seq) if read_seq else 0
    num_mismatches = read.get_tag("NM") if read.has_tag("NM") else None

    return {
        "read_id": read.query_name,
        "fragment_length": frag_length,
        "avg_base_quality": avg_quality,
        "gc_content": gc_content,
        "num_mismatches": num_mismatches,
        "chrom": read.reference_name,
        "start": read.reference_start,
        "end": read.reference_end
    }
