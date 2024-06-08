from Bio.Restriction import AllEnzymes, CommOnly, RestrictionBatch
from Bio.Seq import Seq
from collections import deque

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

def translate_DNA_to_protein_simple(dna_sequence):
    # Create a Seq object
    dna_seq = Seq(dna_sequence)

    # Translate DNA to protein
    protein_seq = dna_seq.translate()

    return str(protein_seq)

def translate_DNA_in_frames(dna_sequence):
    dna_seq = Seq(dna_sequence)

    frames = {
        "Frame 1": str(dna_seq.translate()),
        "Frame 2": str(dna_seq[1:].translate()),
        "Frame 3": str(dna_seq[2:].translate())
    }

    return frames

def extract_possible_proteins_from_protein_sequence(seq):
    '''
    Given protein sequence, return possible protein sequence.
    :param seq: protein string. Start codon is M and stop codon is *
    :return: List of possible protein in (protein string, start index into original sequence)
    '''
    possible_proteins = []
    # (protein sequence string, index into the sequence)
    curr = ("", -1)
    stack = deque()

    for i in range(len(seq)):
        # Start codon encountered
        if seq[i] == 'M':
            if not curr[0] == "":
                stack.append(curr)
            curr = ("M", i)

        # End codon encountered
        elif seq[i] == '*':
            if curr[0] == "":
                continue

            possible_proteins.append((curr[0][1:], curr[1]))
            while len(stack) > 0:
                top = stack.pop()
                curr = (top[0] + curr[0], top[1])
                # append protein sequence, remove the first start codon
                possible_proteins.append((curr[0][1:], curr[1]))

            curr = ("", -1)
        else:
            if curr[0] != "":
                curr = (curr[0] + seq[i], curr[1])

    return possible_proteins

