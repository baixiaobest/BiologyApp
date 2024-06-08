import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QTextEdit, QTabWidget, QHBoxLayout
)
from PyQt5.QtGui import QFont
from Utilities import translate_DNA_in_frames

class DNAToProteinApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DNA to Protein (DNA 转蛋白质)")
        self.resize(800, 600)  # Set the default size of the window

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
        self.proteins_tab_layout = QVBoxLayout(self.proteins_tab)

        self.proteins_output = QTextEdit()
        self.proteins_output.setFont(QFont("Arial", self.text_edit_font_size))
        self.proteins_output.setReadOnly(True)
        self.proteins_tab_layout.addWidget(self.proteins_output)

        self.tabs.addTab(self.proteins_tab, "Possible proteins (可能的蛋白)")

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def translate_dna(self):
        dna_sequence = self.dna_input.toPlainText().strip()

        # Validate the DNA sequence
        if not self.is_valid_dna_sequence(dna_sequence):
            error_message = "Error: Invalid DNA sequence. Please enter a sequence containing only A, T, C, G. \n错误：无效DNA序列。请输入仅包含 A, T, C, G 的序列。"
            self.frame1_output.setText(error_message)
            self.frame2_output.setText("")
            self.frame3_output.setText("")
            self.proteins_output.setText("")
            return

        translations = translate_DNA_in_frames(dna_sequence)
        self.frame1_output.setText(translations["Frame 1"])
        self.frame2_output.setText(translations["Frame 2"])
        self.frame3_output.setText(translations["Frame 3"])

        # Display possible proteins in the proteins tab
        possible_proteins = "\n".join(translations.values())
        self.proteins_output.setText(possible_proteins)

    def is_valid_dna_sequence(self, sequence):
        valid_nucleotides = {'A', 'T', 'C', 'G'}
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DNAToProteinApp()
    window.show()
    sys.exit(app.exec_())
