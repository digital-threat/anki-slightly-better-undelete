from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
from aqt.qt import *

class UndeleteDialog(QDialog):
    def __init__(self, parent=mw):
        super().__init__(parent)
        self.setWindowTitle("Undelete Notes")

        label = QLabel("Some text")

        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Blueberry", "Raspberry", "Strawberry",
                 "Watermelon", "Zucchini"]

        for text in items:
            item = QListWidgetItem(text)
            self.list.addItem(item)

        button = QPushButton("Undelete")
        qconnect(button.clicked, self.onUndeleteButtonClicked)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addWidget(self.list)
        layout.addWidget(button)

        self.setLayout(layout)

    def onUndeleteButtonClicked(self) -> None:
        selected = []

        for item in self.list.selectedItems():
            selected.append(item.text())

        showInfo("\n".join(selected))


def showDialog() -> None:
    dialog = UndeleteDialog()
    dialog.show()

action = QAction("Undelete Notes", mw)
qconnect(action.triggered, showDialog)
mw.form.menuTools.addAction(action)
