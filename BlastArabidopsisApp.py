import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
    QTableWidget, QTableWidgetItem, QSpinBox, QWidget, QHeaderView, QDialog
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from BlastUtilities import blast_sequence_against_database
import os


class BlastArabidopsisApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blast Arabidopsis (拟南芥BLAST)")
        self.resize(900, 800)  # Set the default size of the window

        # Define font size
        self.label_font_size = 10
        self.input_font_size = 10

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a text input widget for DNA sequence
        self.dna_label = QLabel("Input DNA sequence (输入DNA序列):")
        self.dna_label.setFont(QFont("Arial", self.label_font_size))
        main_layout.addWidget(self.dna_label)

        self.dna_input = QTextEdit()
        self.dna_input.setFont(QFont("Arial", self.input_font_size))
        self.dna_input.setMaximumHeight(200)
        main_layout.addWidget(self.dna_input)

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
        main_layout.addLayout(evalue_layout)

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
        main_layout.addLayout(word_size_layout)

        # Create a blast button
        self.blast_button = QPushButton("BLAST")
        self.blast_button.setFont(QFont("Arial", self.label_font_size))
        self.blast_button.clicked.connect(self.on_blast)
        main_layout.addWidget(self.blast_button)

        # Create a message label for validation errors and no results
        self.message_label = QLabel("")
        self.message_label.setFont(QFont("Arial", self.label_font_size))
        self.message_label.setStyleSheet("color: red")
        main_layout.addWidget(self.message_label)

        # Create a result display area
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Query sequence\n(查询序列)",
            "Arabidopsis sequence\n(拟南芥序列)",
            "E value\n(E值)",
            "Length\n(长度)",
            "Gene Name\n(基因名称)",
            "Details\n(详细信息)"
        ])
        header = self.result_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.result_table)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

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

        evalue_exponent = self.evalue_input.value()
        word_size = self.word_size_input.value()

        # Perform BLAST search
        db_path = os.getcwd() + "\\assets\\TAIRBlastDB/TAIRBlastDB"  # Set your BLAST database path

        query_sequence = f">Query\n{dna_sequence}"

        blast_result = blast_sequence_against_database(
            query_sequence,
            db_path,
            evalue=10 ** evalue_exponent,
            word_size=word_size
        )

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
        return title.split()[1]

    def show_details(self, hsp, alignment):
        details_window = DetailsWindow(hsp, alignment, self)
        details_window.show()  # Use show() instead of exec_() to make it non-modal


class DetailsWindow(QDialog):
    def __init__(self, hsp, alignment, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alignment Details (比对详情)")
        self.resize(600, 500)

        layout = QVBoxLayout()

        # Description field
        description_text = (
            f"E value: {hsp.expect}\n"
            f"Length: {hsp.align_length}\n"
            f"Description: {alignment.title}\n"
            f"Query start: {hsp.query_start}\n"
            f"Query end: {hsp.query_end}\n"
            f"Subject start: {hsp.sbjct_start}\n"
            f"Subject end: {hsp.sbjct_end}"
        )
        description_label = QLabel("Description (描述):")
        description_label.setFont(QFont("Arial", 10))
        layout.addWidget(description_label)

        self.description_field = QTextEdit()
        self.description_field.setFont(QFont("Arial", 10))
        self.description_field.setPlainText(description_text)
        self.description_field.setReadOnly(True)
        self.description_field.setMinimumHeight(250)
        layout.addWidget(self.description_field)

        # Matches field
        matches_text = f"Query:   {hsp.query}\n" \
                       f"Matches: {hsp.match}\n" \
                       f"Subject: {hsp.sbjct}"
        matches_label = QLabel("Matches (匹配):")
        matches_label.setFont(QFont("Arial", 10))
        layout.addWidget(matches_label)

        self.matches_field = QTextEdit()
        monospace_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        self.matches_field.setFont(monospace_font)
        self.matches_field.setPlainText(matches_text)
        self.matches_field.setReadOnly(True)
        self.matches_field.setLineWrapMode(QTextEdit.NoWrap)
        layout.addWidget(self.matches_field)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BlastArabidopsisApp()
    window.show()
    sys.exit(app.exec_())
