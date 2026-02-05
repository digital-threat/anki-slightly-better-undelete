from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
from aqt.qt import *

class UndeleteDialog(QDialog):
    def __init__(self, parent=mw):
        super().__init__(parent)
        self.setWindowTitle("Undelete Notes")

        label = QLabel("Some text")
        button = QPushButton("Undelete")
        selectAllBtn = QPushButton("Select All")
        clearSelectionBtn = QPushButton("Clear")

        qconnect(button.clicked, self.onUndeleteButtonClicked)
        qconnect(selectAllBtn.clicked, self.onSelectAllClicked)
        qconnect(clearSelectionBtn.clicked, self.onSelectNoneClicked)

        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        items = ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Blueberry", "Raspberry", "Strawberry",
                 "Watermelon", "Zucchini"]

        for text in items:
            item = QListWidgetItem(text)
            self.list.addItem(item)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(selectAllBtn)
        buttonLayout.addWidget(clearSelectionBtn)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.list)
        layout.addWidget(button)

        self.setLayout(layout)

    def onSelectAllClicked(self) -> None:
        self.list.selectAll()

    def onSelectNoneClicked(self) -> None:
        self.list.clearSelection()

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
