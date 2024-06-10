from Bio.Restriction import AllEnzymes, CommOnly, RestrictionBatch
from Bio.Seq import Seq
from collections import deque
import os
import sys

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

def translate_DNA_to_amino_acids_simple(dna_sequence):
    # Create a Seq object
    dna_seq = Seq(dna_sequence)

    # Translate DNA to protein
    protein_seq = dna_seq.translate()

    return str(protein_seq)

def translate_DNA_to_amino_acids_in_frames(dna_sequence):
    dna_seq = Seq(dna_sequence)

    frames = [
        str(dna_seq.translate()),
        str(dna_seq[1:].translate()),
        str(dna_seq[2:].translate())]

    return frames

def extract_possible_proteins_from_protein_sequence(seq):
    '''
    Given protein sequence, return possible protein sequence.
    :param seq: protein string. Start codon is M and stop codon is *
    :return: List of possible protein in (protein string, start index into original sequence).
    index is 0-indexed.
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
            curr = (curr[0] + "*",  curr[1])
            possible_proteins.append(curr)
            while len(stack) > 0:
                top = stack.pop()
                curr = (top[0] + curr[0], top[1])
                possible_proteins.append(curr)

            curr = ("", -1)
        # Non-start or non-stop codon encountered,
        # and we have encountered start codon before.
        elif curr[0] != "":
            curr = (curr[0] + seq[i], curr[1])

    return possible_proteins

def extract_possible_proteins_from_DNA(dna_seq):
    '''
    Given DNA sequence, extract all possible protein in different frames.
    :param dna_seq: dna sequence in string.
    :return: list of all possible protein and its location information.
        DNA indexing is 1-indexed.
    '''
    frame_aa_seq = translate_DNA_to_amino_acids_in_frames(dna_seq)

    frame_proteins = []

    for idx, amino_acid_seq in enumerate(frame_aa_seq):
        possible_proteins = extract_possible_proteins_from_protein_sequence(amino_acid_seq)
        for protein in possible_proteins:
            protein_seq = protein[0]
            protein_length = len(protein_seq)
            dna_length = len(protein_seq) * 3
            # +1 because it is 1-indexed dna start location.
            # +idx because frame shifting
            dna_start = protein[1] * 3 + 1 + idx
            # 1-indexed dna end location.
            # -1 because it points to the third code of stop codon
            dna_end = dna_start + dna_length - 1

            frame_proteins.append({
                "frame": idx + 1,
                "protein_sequence": protein_seq,
                "protein_length": protein_length,
                "dna_length": dna_length,
                "dna_start": dna_start,
                "dna_end": dna_end
            })

    return frame_proteins

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

