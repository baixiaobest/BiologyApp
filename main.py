from Bio.Restriction import CommOnly, RestrictionBatch
from Bio.Seq import Seq

# Example gene sequence
gene_sequence = "gggaccaaaggctttgcacctttgttgtctcagggctttacttggtctttaattgaatgtacaaagttgatgtaaaagctttggctccatcgttcatggagtctagtacattgttttgggttttaaaagttttctgtgttaaagctcgtcgtctaattgatgttgtgtttggttttagttgaaaggtttagacgtttagtaaaaaagttactcaaattcttgaaatctccttggccttgctgattataaaatcaaatattcatttataaaattatgcgaaagggtctaattatttttgaaaccgaatcgaatgaagacaactccattttgattgattttttttttgttgtattaaagaataaaaaactcgactggttcaacaagactggattgtctttaaactactggttcaatgtattttgggtacataatgaaaaaaatacacaatccgccttggccacgtatccatctttggcttagttgatgatgataatacttttgttttttggtaaggctgatgatgataatagttagaagaagttcatagaataatccaatggatttccaataataaaacacagaaataaatataatccaaacaattgccaaaaataatgaataagaaaagggacccacaccaaaagctaaaagcgcgtgggtcagattacaaaaagcgaaaccccaaaccgtggctagacagcggacgaacccgtcccttcaaacgtggctcacctttcgaaccacagagagcagtttacactccaactgtcaaaaacgtgttcccatgacgtcatcctcaacgtatctttatcactttttaaaactaaagactgttttgtctttttctaaatcgtcccctttctccgaacaccatacttaaattcaataaaataataaatatcaaaactgaaccatcgaatcggaaccagccacagtacacaatacacttagacgaagtaaagtgattcagaaggacacgtgtaagtcacataccgtgggacacttgtcgttaccagatcctccgtgtttctcacttttcttataaaataaaaacacaacacttcttcactttctgtaataaaaatatctccaaaagttccaacacctgaaaacataaaaagatagaaagagaaataaaacatcttatccaaagaaaaa"

def find_restriction_sites(gene_seq):
    # Convert gene sequence to Biopython Seq object
    gene_seq = Seq(gene_seq)

    # Get common restriction enzymes
    enzymes = RestrictionBatch(CommOnly)

    # Find restriction sites
    results = enzymes.search(gene_seq)

    # Separate enzymes into two groups
    matched_enzymes = {enzyme: sites for enzyme, sites in results.items() if sites}
    unmatched_enzymes = {enzyme: sites for enzyme, sites in results.items() if not sites}

    # Sort enzymes alphabetically, ignoring capitalization
    sorted_matched_enzymes = sorted(matched_enzymes.keys(), key=lambda e: e.__name__.lower())
    sorted_unmatched_enzymes = sorted(unmatched_enzymes.keys(), key=lambda e: e.__name__.lower())

    return sorted_matched_enzymes, sorted_unmatched_enzymes

# Find restriction sites
matched_enzymes, unmatched_enzymes = find_restriction_sites(gene_sequence)

# Print results for matched enzymes
for enzyme in matched_enzymes:
    print(f"Enzyme {enzyme} cuts at positions: {enzyme.results}")

# Print results for unmatched enzymes
print("Enzymes that do not cut the gene sequence:")
print([enzyme.__name__ for enzyme in unmatched_enzymes])
