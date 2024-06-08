import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QLabel, QTextEdit, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from Utilities import translate_DNA_in_frames, extract_possible_proteins_from_protein_sequence

class DNAToProteinApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNA to Protein (DNA 转蛋白质)")
        self.resize(1200, 600)  # Set the default size of the window

        # Define font size
        self.label_font_size = 10
        self.text_edit_font_size = 10

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
        self.proteins_tab_layout = QHBoxLayout(self.proteins_tab)

        self.frame1_proteins_table = self.create_protein_table("Frame 1 Proteins (读码框 1 蛋白)")
        self.proteins_tab_layout.addWidget(self.frame1_proteins_table)

        self.frame2_proteins_table = self.create_protein_table("Frame 2 Proteins (读码框 2 蛋白)")
        self.proteins_tab_layout.addWidget(self.frame2_proteins_table)

        self.frame3_proteins_table = self.create_protein_table("Frame 3 Proteins (读码框 3 蛋白)")
        self.proteins_tab_layout.addWidget(self.frame3_proteins_table)

        self.tabs.addTab(self.proteins_tab, "Possible proteins (可能的蛋白)")

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def create_protein_table(self, label_text):
        label = QLabel(label_text)
        label.setFont(QFont("Arial", self.label_font_size))
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Protein sequence\n(蛋白序列)", "Index\n(蛋白位置)"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
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
            self.clear_protein_tables()
            return

        translations = translate_DNA_in_frames(dna_sequence)
        self.frame1_output.setText(translations["Frame 1"])
        self.frame2_output.setText(translations["Frame 2"])
        self.frame3_output.setText(translations["Frame 3"])

        # Display possible proteins in the proteins tab
        possible_proteins = {frame: extract_possible_proteins_from_protein_sequence(seq) for frame, seq in translations.items()}
        self.update_protein_table(self.frame1_proteins_table.findChild(QTableWidget), possible_proteins["Frame 1"])
        self.update_protein_table(self.frame2_proteins_table.findChild(QTableWidget), possible_proteins["Frame 2"])
        self.update_protein_table(self.frame3_proteins_table.findChild(QTableWidget), possible_proteins["Frame 3"])

    def update_protein_table(self, table, proteins):
        table.setRowCount(len(proteins))
        for row, (protein_seq, start_idx) in enumerate(proteins):
            table.setItem(row, 0, QTableWidgetItem(protein_seq))
            table.setItem(row, 1, QTableWidgetItem(str(start_idx)))

    def clear_protein_tables(self):
        self.frame1_proteins_table.findChild(QTableWidget).setRowCount(0)
        self.frame2_proteins_table.findChild(QTableWidget).setRowCount(0)
        self.frame3_proteins_table.findChild(QTableWidget).setRowCount(0)

    def is_valid_dna_sequence(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNAToProteinApp()
    window.show()
    sys.exit(app.exec_())
