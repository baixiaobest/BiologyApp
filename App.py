import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QLineEdit, QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QFont
from RestrictionSites import find_restriction_sites


class RestrictionEnzymeFinder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Restriction Enzyme Finder")
        self.resize(800, 600)  # Set the default size of the window

        # Define font size
        self.label_font_size = 10
        self.text_edit_font_size = 10
        self.table_height = 250  # Fixed height for the tables

        # Create main layout
        main_layout = QVBoxLayout()

        # Create a text input widget
        self.label = QLabel("Enter Gene Sequence:")
        self.label.setFont(QFont("Arial", self.label_font_size))
        main_layout.addWidget(self.label)

        self.text_input = QTextEdit()
        self.text_input.setFont(QFont("Arial", self.text_edit_font_size))
        self.text_input.setLineWrapMode(QTextEdit.WidgetWidth)
        main_layout.addWidget(self.text_input)

        # Create a submit button
        self.submit_button = QPushButton("Find Restriction Sites")
        self.submit_button.setFont(QFont("Arial", self.label_font_size))
        self.submit_button.clicked.connect(self.on_submit)
        main_layout.addWidget(self.submit_button)

        # Create a results layout
        self.results_layout = QVBoxLayout()
        main_layout.addLayout(self.results_layout)

        # Create an error message label
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Arial", self.label_font_size))
        self.error_label.setStyleSheet("color: red")
        main_layout.addWidget(self.error_label)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def on_submit(self):
        gene_sequence = self.text_input.toPlainText().strip().upper()

        # Validate the gene sequence
        if not self.is_valid_dna_sequence(gene_sequence):
            self.error_label.setText("Error: Invalid DNA sequence. Please enter a sequence containing only A, T, C, G.")
            self.clear_results()
            return
        else:
            self.error_label.setText("")  # Clear any previous error messages

        self.matched_enzymes, self.matched_sites, self.unmatched_enzymes = find_restriction_sites(gene_sequence)

        self.clear_results()

        # Create the filter input after a successful submission
        self.filter_label = QLabel("Filter Enzymes:")
        self.filter_label.setFont(QFont("Arial", self.label_font_size))
        self.results_layout.addWidget(self.filter_label)

        self.filter_input = QLineEdit()
        self.filter_input.setFont(QFont("Arial", self.text_edit_font_size))
        self.filter_input.textChanged.connect(self.on_filter)
        self.results_layout.addWidget(self.filter_input)

        self.update_results()

    def is_valid_dna_sequence(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        return all(nucleotide in valid_nucleotides for nucleotide in sequence)

    def clear_results(self):
        for i in reversed(range(self.results_layout.count())):
            widget_to_remove = self.results_layout.itemAt(i).widget()
            self.results_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def on_filter(self):
        self.update_results()

    def update_results(self):
        filter_text = self.filter_input.text().strip().lower()

        # Clear previous results but keep filter
        for i in reversed(range(2, self.results_layout.count())):
            widget_to_remove = self.results_layout.itemAt(i).widget()
            self.results_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Filter matched enzymes
        filtered_matched_enzymes = [
            enzyme for enzyme in self.matched_enzymes
            if filter_text in enzyme.__name__.lower()
        ]

        # Filter unmatched enzymes
        filtered_unmatched_enzymes = [
            enzyme for enzyme in self.unmatched_enzymes
            if filter_text in enzyme.__name__.lower()
        ]

        # Display results for matched enzymes
        matched_label = QLabel("Matched Enzymes:")
        matched_label.setFont(QFont("Arial", self.label_font_size))
        self.results_layout.addWidget(matched_label)

        matched_table = QTableWidget()
        matched_table.setColumnCount(3)
        matched_table.setHorizontalHeaderLabels(["Enzyme", "Cut Positions", "Sequence"])
        matched_table.setRowCount(len(filtered_matched_enzymes))

        for i, enzyme in enumerate(filtered_matched_enzymes):
            matches = self.matched_sites[enzyme]
            matched_table.setItem(i, 0, QTableWidgetItem(enzyme.__name__))
            matched_table.setItem(i, 1, QTableWidgetItem(str(matches)))
            matched_table.setItem(i, 2, QTableWidgetItem(str(enzyme.site)))

        # Make the table stretch to fit the container width
        header = matched_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        matched_table.setFixedHeight(self.table_height)
        self.results_layout.addWidget(matched_table)

        # Display results for unmatched enzymes
        unmatched_label = QLabel("Enzymes that do not cut the gene sequence:")
        unmatched_label.setFont(QFont("Arial", self.label_font_size))
        self.results_layout.addWidget(unmatched_label)

        unmatched_table = QTableWidget()
        unmatched_table.setColumnCount(2)
        unmatched_table.setHorizontalHeaderLabels(["Enzyme", "Sequence"])
        unmatched_table.setRowCount(len(filtered_unmatched_enzymes))

        for i, enzyme in enumerate(filtered_unmatched_enzymes):
            unmatched_table.setItem(i, 0, QTableWidgetItem(enzyme.__name__))
            unmatched_table.setItem(i, 1, QTableWidgetItem(str(enzyme.site)))

        # Make the table stretch to fit the container width
        header = unmatched_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        unmatched_table.setFixedHeight(self.table_height)
        self.results_layout.addWidget(unmatched_table)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RestrictionEnzymeFinder()
    window.show()
    sys.exit(app.exec_())
