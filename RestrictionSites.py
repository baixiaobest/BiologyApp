from Bio.Restriction import AllEnzymes, CommOnly, RestrictionBatch
from Bio.Seq import Seq

def find_restriction_sites(gene_seq):
    # Convert gene sequence to Biopython Seq object
    gene_seq = Seq(gene_seq)

    # Get common restriction enzymes
    enzymes = RestrictionBatch(AllEnzymes)

    # Find restriction sites
    results = enzymes.search(gene_seq)

    # Separate enzymes into two groups
    matched_enzymes = {enzyme: sites for enzyme, sites in results.items() if sites}
    unmatched_enzymes = {enzyme: sites for enzyme, sites in results.items() if not sites}

    # Sort enzymes alphabetically, ignoring capitalization
    sorted_matched_enzymes = sorted(matched_enzymes.keys(), key=lambda e: e.__name__.lower())
    sorted_unmatched_enzymes = sorted(unmatched_enzymes.keys(), key=lambda e: e.__name__.lower())

    return sorted_matched_enzymes, matched_enzymes, sorted_unmatched_enzymes
