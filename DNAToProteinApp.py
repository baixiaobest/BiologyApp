import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox
)
from PyQt5.QtGui import QFont
from Utilities import translate_DNA_to_amino_acids_in_frames, extract_possible_proteins_from_DNA

class DNAToProteinApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNA to Protein (DNA 转蛋白质)")
        self.resize(1200, 600)  # Set the default size of the window

        # Define font size
        self.label_font_size = 10
        self.text_edit_font_size = 10

        # Initialize possible proteins
        self.possible_proteins = None

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a text input widget for DNA sequence
        self.label = QLabel("DNA Sequence (DNA 序列):")
        self.label.setFont(QFont("Arial", self.label_font_size))
        main_layout.addWidget(self.label)

        self.dna_input = QTextEdit()
        self.dna_input.setFont(QFont("Arial", self.text_edit_font_size))
        self.dna_input.setLineWrapMode(QTextEdit.WidgetWidth)
        self.dna_input.setMaximumHeight(250)
        main_layout.addWidget(self.dna_input)

        # Create a button to translate DNA to protein
        self.translate_button = QPushButton("Translate to Protein (转化为蛋白质)")
        self.translate_button.setFont(QFont("Arial", self.label_font_size))
        self.translate_button.clicked.connect(self.translate_dna)
        main_layout.addWidget(self.translate_button)

        # Create tabs
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial", self.label_font_size))
        main_layout.addWidget(self.tabs)

        # Create Sequence tab
        self.sequence_tab = QWidget()
        self.sequence_tab_layout = QVBoxLayout(self.sequence_tab)

        self.frame1_label = QLabel("Frame 1 (读码框 1):")
        self.frame1_label.setFont(QFont("Arial", self.label_font_size))
        self.sequence_tab_layout.addWidget(self.frame1_label)

        self.frame1_output = QTextEdit()
        self.frame1_output.setFont(QFont("Arial", self.text_edit_font_size))
        self.frame1_output.setReadOnly(True)
        self.sequence_tab_layout.addWidget(self.frame1_output)

        self.frame2_label = QLabel("Frame 2 (读码框 2):")
        self.frame2_label.setFont(QFont("Arial", self.label_font_size))
        self.sequence_tab_layout.addWidget(self.frame2_label)

        self.frame2_output = QTextEdit()
        self.frame2_output.setFont(QFont("Arial", self.text_edit_font_size))
        self.frame2_output.setReadOnly(True)
        self.sequence_tab_layout.addWidget(self.frame2_output)

        self.frame3_label = QLabel("Frame 3 (读码框 3):")
        self.frame3_label.setFont(QFont("Arial", self.label_font_size))
        self.sequence_tab_layout.addWidget(self.frame3_label)

        self.frame3_output = QTextEdit()
        self.frame3_output.setFont(QFont("Arial", self.text_edit_font_size))
        self.frame3_output.setReadOnly(True)
        self.sequence_tab_layout.addWidget(self.frame3_output)

        self.tabs.addTab(self.sequence_tab, "Sequence (翻译序列)")

        # Create Possible Proteins tab
        self.proteins_tab = QWidget()
        self.proteins_tab_layout = QVBoxLayout(self.proteins_tab)

        filter_layout = QHBoxLayout()
        self.filter_label = QLabel("Filter DNA Length (过滤 DNA 长度):")
        self.filter_label.setFont(QFont("Arial", self.label_font_size))
        filter_layout.addWidget(self.filter_label)

        self.dna_length_filter = QSpinBox()
        self.dna_length_filter.setFont(QFont("Arial", self.label_font_size))
        self.dna_length_filter.setFixedWidth(100)  # Set the fixed width
        self.dna_length_filter.setRange(0, 100000)  # Set an appropriate range for DNA length
        self.dna_length_filter.valueChanged.connect(self.apply_filter)
        filter_layout.addWidget(self.dna_length_filter)

        self.proteins_tab_layout.addLayout(filter_layout)

        self.proteins_table = self.create_protein_table("Possible Proteins (可能的蛋白)")
        self.proteins_tab_layout.addWidget(self.proteins_table)

        self.tabs.addTab(self.proteins_tab, "Possible proteins (可能的蛋白)")

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_protein_table(self, label_text):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", self.label_font_size))
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Protein sequence\n(蛋白序列)",
            "Protein length\n(蛋白长度)",
            "DNA length\n(DNA长度)",
            "DNA start\n(起始位置)",
            "DNA end\n(结束位置)",
            "Frame\n(读码框)"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(table)
        container = QWidget()
        container.setLayout(layout)
        return container

    def translate_dna(self):
        dna_sequence = self.dna_input.toPlainText().strip()

        # Validate the DNA sequence
        if not self.is_valid_dna_sequence(dna_sequence):
            error_message = "Error: Invalid DNA sequence. Please enter a sequence containing only A, T, C, G. \n错误：无效DNA序列。请输入仅包含 A, T, C, G 的序列。"
            self.frame1_output.setText(error_message)
            self.frame2_output.setText("")
            self.frame3_output.setText("")
            self.clear_protein_table()
            return

        translations = translate_DNA_to_amino_acids_in_frames(dna_sequence)
        self.frame1_output.setText(translations[0])
        self.frame2_output.setText(translations[1])
        self.frame3_output.setText(translations[2])

        # Display possible proteins in the proteins tab
        self.possible_proteins = extract_possible_proteins_from_DNA(dna_sequence)
        self.apply_filter()

    def apply_filter(self):
        if self.possible_proteins is None:
            return
        filter_length = self.dna_length_filter.value()
        filtered_proteins = [protein for protein in self.possible_proteins if protein["dna_length"] >= filter_length]
        self.update_protein_table(self.proteins_table.findChild(QTableWidget), filtered_proteins)

    def update_protein_table(self, table, proteins):
        table.setRowCount(len(proteins))
        for row, protein in enumerate(proteins):
            table.setItem(row, 0, QTableWidgetItem(protein["protein_sequence"]))
            table.setItem(row, 1, QTableWidgetItem(str(protein["protein_length"])))
            table.setItem(row, 2, QTableWidgetItem(str(protein["dna_length"])))
            table.setItem(row, 3, QTableWidgetItem(str(protein["dna_start"])))
            table.setItem(row, 4, QTableWidgetItem(str(protein["dna_end"])))
            table.setItem(row, 5, QTableWidgetItem(str(protein["frame"])))

    def clear_protein_table(self):
        self.proteins_table.findChild(QTableWidget).setRowCount(0)

    def is_valid_dna_sequence(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNAToProteinApp()
    window.show()
    sys.exit(app.exec_())
