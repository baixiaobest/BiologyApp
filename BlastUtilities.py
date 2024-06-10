import os
import subprocess
import tempfile
from Bio.Blast import NCBIXML
from Bio import SeqIO
from io import StringIO

def print_blast_results(blast_record):
    if blast_record.alignments:
        for alignment in blast_record.alignments:
            for hsp in alignment.hsps:
                print(f"****Alignment****")
                print(f"sequence: {alignment.title}")
                print(f"length: {alignment.length}")
                print(f"e value: {hsp.expect}")
                print(f"Query:   {hsp.query}")
                print(f"Match:   {hsp.match}")
                print(f"Subject: {hsp.sbjct}")
    else:
        print("No alignments found.")

def combine_fasta_files(folder_path, combined_file_path):
    with open(combined_file_path, 'w') as combined_file:
        for filename in os.listdir(folder_path):
            if filename.endswith(".fasta") or filename.endswith(".fa"):
                file_path = os.path.join(folder_path, filename)
                print(filename)
                with open(file_path, 'r') as fasta_file:
                    for record in SeqIO.parse(fasta_file, "fasta"):
                        record.description += f" [source={filename}]"
                        SeqIO.write(record, combined_file, "fasta")

def create_blast_database(subject_file_path, db_path):
    makeblastdb_cmd = ["makeblastdb", "-in", subject_file_path, "-dbtype", "nucl", "-out", db_path]
    makeblastdb_result = subprocess.run(makeblastdb_cmd, capture_output=True, text=True)
    if makeblastdb_result.returncode != 0:
        print("Error creating BLAST database")
        exit()

def perform_blast_search(query_file_path, db_path, task="blastn", dust="no",
                         evalue=10, reward=1, penalty=-2, gapopen=5, gapextend=2, word_size=11):
    # Adjusting parameters to ensure more sensitive search
    blastn_cmd = [
        "blastn",
        "-query", query_file_path,
        "-db", db_path,
        "-outfmt", "5",
        "-task", task,  # Using default blastn task for exact matches
        "-dust", dust,      # Disabling low-complexity filter
        "-evalue", str(evalue),  # Setting a high e-value threshold to ensure hits are not filtered out
        "-reward", str(reward),  # Match reward
        "-penalty", str(penalty),  # Mismatch penalty
        "-gapopen", str(gapopen),  # Default gap open penalty
        "-gapextend", str(gapextend),  # Default gap extension penalty
        "-word_size", str(word_size)  # Word size
    ]
    blastn_result = subprocess.run(blastn_cmd, capture_output=True, text=True)

    if blastn_result.returncode != 0:
        return {
            "returncode": blastn_result.returncode,
            "stderr": blastn_result.stderr
        }

    result_handle = StringIO(blastn_result.stdout)
    blast_record = NCBIXML.read(result_handle)
    return {
        "returncode": 0,
        "blast_record": blast_record
    }

def blast_sequence_against_database(query_sequence, db_path, **kwargs):
    with tempfile.TemporaryDirectory() as tmpdirname:
        query_file_path = os.path.join(tmpdirname, "query.fasta")
        # Write query sequence to a temporary file
        with open(query_file_path, "w") as query_file:
            query_file.write(query_sequence)
        # Perform BLAST search
        return perform_blast_search(query_file_path, db_path, **kwargs)

def blast_two_DNA(sequence1, sequence2, **kwargs):
    # Create temporary directory to store the files
    with tempfile.TemporaryDirectory() as tmpdirname:
        query_file_path = f"{tmpdirname}/query.fasta"
        subject_file_path = f"{tmpdirname}/subject.fasta"
        db_path = f"{tmpdirname}/subject_db"

        # Write sequences to temporary files
        with open(query_file_path, "w") as query_file:
            query_file.write(sequence1)

        with open(subject_file_path, "w") as subject_file:
            subject_file.write(sequence2)

        # Create BLAST database
        create_blast_database(subject_file_path, db_path)

        # Perform BLAST search
        return perform_blast_search(query_file_path, db_path, **kwargs)
