import unittest
from Utilities import extract_possible_proteins_from_protein_sequence

class MyTestCase(unittest.TestCase):
    def test_extract_possible_proteins_from_protein_sequence(self):
        protein_seq1 = "Mabc*"
        protein_list1 = [("abc", 0)]

        protein_seq2 = "dfcMMabc*"
        protein_list2 = [("abc", 4), ("Mabc",3)]

        protein_seq3 = "adeMdcde**"
        protein_list3 = [("dcde", 3)]

        protein_seq4 = "adMadefcMefde*ded*sdf"
        protein_list4 = [("efde", 8), ("adefcMefde", 2)]

        res1 = extract_possible_proteins_from_protein_sequence(protein_seq1)
        self.check(res1, protein_list1)

        res2 = extract_possible_proteins_from_protein_sequence(protein_seq2)
        self.check(res2, protein_list2)

        res3 = extract_possible_proteins_from_protein_sequence(protein_seq3)
        self.check(res3, protein_list3)

        res4 = extract_possible_proteins_from_protein_sequence(protein_seq4)
        self.check(res4, protein_list4)

    def check(self, list1, list2):
        self.assertEqual(len(list1), len(list2))

        for item in list1:
            self.assertTrue(item in list2)  # add assertion here


if __name__ == '__main__':
    unittest.main()
