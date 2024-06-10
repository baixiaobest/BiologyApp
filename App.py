import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QSize, Qt
from RestrictionEnzymeFinderApp import RestrictionEnzymeFinder
from DNAToProteinApp import DNAToProteinApp
from BlastArabidopsisApp import BlastArabidopsisApp

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Genetic Engineering Toolbox (基因工程工具箱)")
        self.resize(600, 300)  # Set the default size of the window

        # Define font size
        self.button_font_size = 8

        # Create main layout
        main_layout = QGridLayout()

        # Create a button to launch the RestrictionEnzymeFinder app
        self.restriction_sites_button = self.create_button("Restriction Sites Finder\n (酶切位点搜寻)")
        self.restriction_sites_button.clicked.connect(self.launch_restriction_enzyme_finder)
        main_layout.addWidget(self.restriction_sites_button, 0, 0)  # Top-left corner

        # Create a button to launch the DNAToProtein app
        self.dna_to_protein_button = self.create_button("DNA to Protein\n (DNA 转蛋白质)")
        self.dna_to_protein_button.clicked.connect(self.launch_dna_to_protein)
        main_layout.addWidget(self.dna_to_protein_button, 0, 1)

        # Create a button to launch the BlastArabidopsis app
        self.blast_arabidopsis_button = self.create_button("BLAST Arabidopsis\n (拟南芥BLAST)")
        self.blast_arabidopsis_button.clicked.connect(self.launch_blast_arabidopsis)
        main_layout.addWidget(self.blast_arabidopsis_button, 0, 2)

        # Create a placeholder button for Protein Comparison (not implemented yet)
        self.protein_comparison_button = self.create_button("Protein Comparison\n (蛋白质比较)")
        main_layout.addWidget(self.protein_comparison_button, 0, 3)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.restriction_enzyme_finder_window = None
        self.dna_to_protein_window = None
        self.blast_arabidopsis_window = None

    def create_button(self, text):
        button = QPushButton()
        button.setFixedSize(QSize(150, 150))  # Make it a square button
        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        layout = QVBoxLayout(button)
        label = QLabel(text)
        label.setFont(QFont("Arial", self.button_font_size))
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        layout.addWidget(label)

        return button

    def launch_restriction_enzyme_finder(self):
        if self.restriction_enzyme_finder_window is None or not self.restriction_enzyme_finder_window.isVisible():
            self.restriction_enzyme_finder_window = RestrictionEnzymeFinder()
        self.restriction_enzyme_finder_window.show()

    def launch_dna_to_protein(self):
        if self.dna_to_protein_window is None or not self.dna_to_protein_window.isVisible():
            self.dna_to_protein_window = DNAToProteinApp()
        self.dna_to_protein_window.show()

    def launch_blast_arabidopsis(self):
        if self.blast_arabidopsis_window is None or not self.blast_arabidopsis_window.isVisible():
            self.blast_arabidopsis_window = BlastArabidopsisApp()
        self.blast_arabidopsis_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
