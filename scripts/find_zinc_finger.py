import re

def find_zinc_finger_sequences(protein_sequence):
    # Define regular expression patterns for various zinc finger motifs
    patterns = {
        'C2H2': r'C.{2}C.{3}[FY].{5}L.{2}H.{3}H',
        'C4': r'C.{2}C.{13}C.{2}C',
        'C6': r'C.{2}C.{6}C.{6}C',
        'LIM': r'C.{2}C.{16,23}H.{2}H',
        'PHD': r'C.{2}C.{11,14}C.{2}C',
        'RING': r'C.{2}C.{9,39}C.{1,3}H.{2,3}C.{2}C.{4,48}C.{2}C',
        'GATA': r'C.{2}C.{17}C.{2}C'
    }

    matches = {}
    for motif, pattern in patterns.items():
        matches[motif] = [(match.start(), match.end(), match.group()) for match in re.finditer(pattern, protein_sequence)]

    return matches

def main():
    # Example sequence to search within
    sequence = "MDETNGRRETHDFMNVNVESFSQLPFIRRTPPKEKAAIIRLFGQELVGDNSDNLSAEPSDHQTTTKNDESSENIKDKDKEKDKDKDKDNNNNRRFECHYCFRNFPTSQALGGHQNAHKRERQHAKRGSMTSYLHHHQPHDPHHIYGFLNNHHHRHYPSWTTEARSYYGGGGHQTPSYYSRNTLAPPSSNPPTINGSPLGLWRVPPSTSTNTIQGVYSSSPASAFRSHEQETNKEPNNWPYRLMKPNVQDHVSLDLHL"

    # Find zinc finger sequences
    zinc_finger_matches = find_zinc_finger_sequences(sequence)

    # Print the start and end indices along with the matching sequence
    for motif, matches in zinc_finger_matches.items():
        print(f"Motif: {motif}")
        for start, end, match in matches:
            print(f"  Match found: {match} at indices {start} to {end}")

if __name__ == "__main__":
    main()
