from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QFont, QFontDatabase

class DetailsWindow(QDialog):
    def __init__(self, hsp, alignment, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Alignment Details (比对详情)")
        self.resize(800, 600)

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
        self.description_field.setMaximumHeight(250)
        layout.addWidget(self.description_field)

        # Matches field
        matches_text = self.format_matches_text(hsp.query, hsp.match, hsp.sbjct)
        matches_label = QLabel("Matches (匹配):")
        matches_label.setFont(QFont("Arial", 10))
        layout.addWidget(matches_label)

        self.matches_field = QTextEdit()
        monospace_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        monospace_font.setPixelSize(20)
        self.matches_field.setFont(monospace_font)
        self.matches_field.setPlainText(matches_text)
        self.matches_field.setReadOnly(True)
        self.matches_field.setLineWrapMode(QTextEdit.NoWrap)
        layout.addWidget(self.matches_field)

        self.setLayout(layout)

    def format_matches_text(self, query, match, subject):
        formatted_text = []
        line_length = 50

        formatted_text.append("query:   ")
        formatted_text.append("matches: ")
        formatted_text.append("subject: ")
        formatted_text.append("")

        for i in range(0, len(query), line_length):
            q_seq = query[i:i + line_length]
            m_seq = match[i:i + line_length]
            s_seq = subject[i:i + line_length]

            formatted_text.append(f"[{i + 1}-{min(len(query), i + 1 + line_length)}]")
            formatted_text.append(f"{q_seq}")
            formatted_text.append(m_seq)
            formatted_text.append(f"{s_seq}")
            formatted_text.append("")

        return "\n".join(formatted_text)
