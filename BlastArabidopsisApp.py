import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QTableWidget, QTableWidgetItem, QSpinBox, QWidget, QHeaderView, QComboBox
)
from PyQt5.QtGui import QFont
from BlastUtilities import blast_sequence_against_database, blast_two_DNA
from Utilities import resource_path
from DetailsWindow import DetailsWindow

class BlastArabidopsisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blast Arabidopsis (拟南芥BLAST)")
        self.resize(900, 800)  # Set the default size of the window

        # Define font size
        self.label_font_size = 10
        self.input_font_size = 10

        # Create main layout
        self.main_layout = QVBoxLayout()

        # Create a text input widget for DNA sequence
        self.dna_label = QLabel("Input DNA sequence (输入DNA序列):")
        self.dna_label.setFont(QFont("Arial", self.label_font_size))
        self.main_layout.addWidget(self.dna_label)

        self.dna_input = QTextEdit()
        self.dna_input.setFont(QFont("Arial", self.input_font_size))
        self.dna_input.setMaximumHeight(200)
        self.main_layout.addWidget(self.dna_input)

        # Create a dropdown for selecting BLAST target
        self.blast_target_label = QLabel("Blast against: (BLAST对象):")
        self.blast_target_label.setFont(QFont("Arial", self.label_font_size))
        self.main_layout.addWidget(self.blast_target_label)

        self.blast_target_dropdown = QComboBox()
        self.blast_target_dropdown.addItems(["Arabidopsis", "Input DNA"])
        self.blast_target_dropdown.setFont(QFont("Arial", self.input_font_size))
        self.blast_target_dropdown.currentIndexChanged.connect(self.on_blast_target_changed)
        self.main_layout.addWidget(self.blast_target_dropdown)

        # Create a text input widget for the second DNA sequence
        self.dna_input_2_label = QLabel("Input second DNA sequence (输入第二DNA序列):")
        self.dna_input_2_label.setFont(QFont("Arial", self.label_font_size))
        self.dna_input_2 = QTextEdit()
        self.dna_input_2.setFont(QFont("Arial", self.input_font_size))
        self.dna_input_2.setMaximumHeight(200)

        # Create a numeric input for E value
        evalue_layout = QHBoxLayout()
        self.evalue_label = QLabel("E value (E值): 1x10^")
        self.evalue_label.setFont(QFont("Arial", self.label_font_size))
        evalue_layout.addWidget(self.evalue_label)

        self.evalue_input = QSpinBox()
        self.evalue_input.setFont(QFont("Arial", self.input_font_size))
        self.evalue_input.setRange(-20, 5)  # Typical range for E-value exponent
        self.evalue_input.setValue(0)  # Default value
        evalue_layout.addWidget(self.evalue_input)
        evalue_layout.addStretch()
        self.main_layout.addLayout(evalue_layout)

        # Create a numeric input for word size
        word_size_layout = QHBoxLayout()
        self.word_size_label = QLabel("Word size (过滤匹配长度):")
        self.word_size_label.setFont(QFont("Arial", self.label_font_size))
        word_size_layout.addWidget(self.word_size_label)

        self.word_size_input = QSpinBox()
        self.word_size_input.setFont(QFont("Arial", self.input_font_size))
        self.word_size_input.setRange(2, 50)  # Typical range for word size
        self.word_size_input.setValue(11)  # Default value
        word_size_layout.addWidget(self.word_size_input)
        word_size_layout.addStretch()
        self.main_layout.addLayout(word_size_layout)

        # Create a blast button
        self.blast_button = QPushButton("BLAST")
        self.blast_button.setFont(QFont("Arial", self.label_font_size))
        self.blast_button.clicked.connect(self.on_blast)
        self.main_layout.addWidget(self.blast_button)

        # Create a message label for validation errors and no results
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Arial", self.label_font_size))
        self.message_label.setStyleSheet("color: red")
        self.main_layout.addWidget(self.message_label)

        # Create a result display area
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Query sequence\n(查询序列)",
            "Subject sequence\n(比对序列)",
            "E value\n(E值)",
            "Length\n(长度)",
            "Gene Name\n(基因名称)",
            "Details\n(详细信息)"
        ])
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.result_table)

        # Set the central widget
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def on_blast_target_changed(self, index):
        if index == 1:  # "Input DNA" selected
            self.main_layout.insertWidget(4, self.dna_input_2_label)
            self.main_layout.insertWidget(5, self.dna_input_2)
        else:
            self.main_layout.removeWidget(self.dna_input_2_label)
            self.dna_input_2_label.setParent(None)
            self.main_layout.removeWidget(self.dna_input_2)
            self.dna_input_2.setParent(None)

    def on_blast(self):
        dna_sequence = self.dna_input.toPlainText().strip()

        # Check for empty input
        if not dna_sequence:
            self.message_label.setText("Input DNA sequence cannot be empty.\n输入DNA序列不能为空。")
            self.result_table.setRowCount(0)
            return

        # Validate the DNA sequence
        if not self.is_valid_dna_sequence(dna_sequence):
            self.message_label.setText(
                "Invalid DNA sequence. Please enter a sequence containing only A, T, C, G.\n无效DNA序列。请输入仅包含A, T, C, G的序列。")
            self.result_table.setRowCount(0)
            return

        blast_target = self.blast_target_dropdown.currentText()
        evalue_exponent = self.evalue_input.value()
        word_size = self.word_size_input.value()

        if blast_target == "Arabidopsis":
            # Perform BLAST search against Arabidopsis
            db_path = resource_path("assets\\TAIRBlastDB/TAIRBlastDB")  # Set your BLAST database path
            query_sequence = f">Query\n{dna_sequence}"
            blast_result = blast_sequence_against_database(
                query_sequence,
                db_path,
                evalue=10 ** evalue_exponent,
                word_size=word_size
            )
        else:
            # Perform BLAST search against input DNA
            dna_sequence_2 = self.dna_input_2.toPlainText().strip()

            # Check for empty second input
            if not dna_sequence_2:
                self.message_label.setText("Second input DNA sequence cannot be empty.\n第二输入DNA序列不能为空。")
                self.result_table.setRowCount(0)
                return

            # Validate the second DNA sequence
            if not self.is_valid_dna_sequence(dna_sequence_2):
                self.message_label.setText(
                    "Invalid second DNA sequence. Please enter a sequence containing only A, T, C, G.\n无效第二DNA序列。请输入仅包含A, T, C, G的序列。")
                self.result_table.setRowCount(0)
                return

            query_sequence = f">Query\n{dna_sequence}"
            subject_sequence = f">Subject\n{dna_sequence_2}"
            blast_result = blast_two_DNA(query_sequence, subject_sequence)

        if blast_result["returncode"] != 0:
            self.message_label.setText(f"Error: {blast_result['stderr']}")
            self.result_table.setRowCount(0)
        else:
            self.display_results(blast_result["blast_record"])

    def is_valid_dna_sequence(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

    def display_results(self, blast_record):
        self.result_table.setRowCount(0)  # Clear previous results

        if not blast_record.alignments:
            self.message_label.setText("No results found (未找到结果).")
            return

        self.message_label.setText("")  # Clear any previous messages

        for alignment in blast_record.alignments:
            gene_name = self.extract_gene_name(alignment.title)
            for hsp in alignment.hsps:
                row_position = self.result_table.rowCount()
                self.result_table.insertRow(row_position)
                self.result_table.setItem(row_position, 0, QTableWidgetItem(hsp.query))
                self.result_table.setItem(row_position, 1, QTableWidgetItem(hsp.sbjct))
                self.result_table.setItem(row_position, 2, QTableWidgetItem(str(hsp.expect)))
                self.result_table.setItem(row_position, 3, QTableWidgetItem(str(hsp.align_length)))
                self.result_table.setItem(row_position, 4, QTableWidgetItem(gene_name))

                details_button = QPushButton("Details (详细信息)")
                details_button.clicked.connect(
                    lambda _, hsp=hsp, alignment=alignment: self.show_details(hsp, alignment))
                self.result_table.setCellWidget(row_position, 5, details_button)

    def extract_gene_name(self, title):
        # This function can be customized to extract gene name from the alignment title.
        # The implementation can vary depending on the title format.
        return title.split()[1]  # Adjusted example: extracting the second word as gene name.

    def show_details(self, hsp, alignment):
        details_window = DetailsWindow(hsp, alignment, self)
        details_window.show()  # Use show() instead of exec_() to make it non-modal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlastArabidopsisApp()
    window.show()
    sys.exit(app.exec_())
