import unittest
from Utilities import *

class MyTestCase(unittest.TestCase):
    def test_extract_possible_proteins_from_protein_sequence(self):
        protein_seq1 = "Mabc*"
        protein_list1 = [("Mabc*", 0)]

        protein_seq2 = "dfcMMabc*"
        protein_list2 = [("Mabc*", 4), ("MMabc*",3)]

        protein_seq3 = "adeMdcde**"
        protein_list3 = [("Mdcde*", 3)]

        protein_seq4 = "adMadefcMefde*ded*sdf"
        protein_list4 = [("Mefde*", 8), ("MadefcMefde*", 2)]

        protein_seq5 = "abdskjej*"
        protein_list5 = []

        res1 = extract_possible_proteins_from_protein_sequence(protein_seq1)
        self.check(res1, protein_list1)

        res2 = extract_possible_proteins_from_protein_sequence(protein_seq2)
        self.check(res2, protein_list2)

        res3 = extract_possible_proteins_from_protein_sequence(protein_seq3)
        self.check(res3, protein_list3)

        res4 = extract_possible_proteins_from_protein_sequence(protein_seq4)
        self.check(res4, protein_list4)

        res5 = extract_possible_proteins_from_protein_sequence(protein_seq5)
        self.check(res5, protein_list5)

    def check(self, list1, list2):
        self.assertEqual(len(list1), len(list2))

        for item in list1:
            self.assertTrue(item in list2)  # add assertion here

    def test_extract_possible_proteins_from_DNA(self):
        # Test case 1: Simple sequence with one protein
        dna_sequence = "ATGTAA"
        expected_result = [
            {
                "frame": 1,
                "protein_sequence": "M*",
                "protein_length": 2,
                "dna_length": 6,
                "dna_start": 1,
                "dna_end": 6
            }
        ]
        self.assertEqual(extract_possible_proteins_from_DNA(dna_sequence), expected_result)

        # Test case 2: Sequence with shifted frames
        dna_sequence = "TATGGGCATGTACAAGTAAGCATGA"
        expected_result = [
            {
                "frame": 2,
                "protein_sequence": "MYK*",
                "protein_length": 4,
                "dna_length": 12,
                "dna_start": 8,
                "dna_end": 19
            },
            {
                "frame": 2,
                "protein_sequence": "MGMYK*",
                "protein_length": 6,
                "dna_length": 18,
                "dna_start": 2,
                "dna_end": 19
            },
        ]
        self.assertEqual(extract_possible_proteins_from_DNA(dna_sequence), expected_result)

        # Test case 3: Sequence with no start codon
        dna_sequence = "TAA"
        expected_result = []
        self.assertEqual(extract_possible_proteins_from_DNA(dna_sequence), expected_result)


if __name__ == '__main__':
    unittest.main()
