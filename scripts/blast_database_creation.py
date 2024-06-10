import os
from BlastUtilities import *
import tempfile

def create_permanent_blast_database(folder_path, db_path):
    combined_fasta_path = os.path.join(db_path, "combined_sequences.fasta")
    # Combine all FASTA files in the folder
    print("Combining fastas...")
    combine_fasta_files(folder_path, combined_fasta_path)
    # Create BLAST database
    print("Creating database")
    create_blast_database(combined_fasta_path, db_path)

if __name__ == "__main__":
    # Get the current working directory and modify the folder path
    folder_path = os.getcwd()
    folder_path += "\\..\\assets\\TAIRBlastSet"
    print(f"Using folder: {folder_path}")

    db_path = os.getcwd() + "\\..\\assets\\TAIRBlastDB/TAIRBlastDB"
    print(f"Using db_path: {db_path}")

    # Create permanent BLAST database
    # create_permanent_blast_database(folder_path, db_path)
    # print(f"BLAST database created at: {db_path}")

    query_sequence = """>QuerySequence
TATCCTAAGGGAAACGTTTTACAATTGCGCTCTGATACGCTAAAGAGAC
TCGATATCAATGAGTTTATTGACGTTGTGATTTATGCACCTCTACTCCAGTGTCTGAGGGCTAAGATGTACTCAACAAAG
AACTTTCAGATCATCAGTTCGGGTTTCCCTGCCAAACTAGATATTGATTT"""

    # Perform BLAST search
    blast_record = blast_sequence_against_database(query_sequence, db_path, word_size=10)
    print_blast_results(blast_record)
