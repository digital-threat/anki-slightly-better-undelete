from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from anki.notes import Note
import os

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

        path = os.path.join(mw.col.path.replace("collection.anki2", ""), "deleted.txt")
        file = open(path, 'r', encoding="utf-8")
        next(file)
        for line in file:
            line = line.rstrip("\n")

            item = QListWidgetItem(line)
            self.list.addItem(item)
        file.close()

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(selectAllBtn)
        buttonLayout.addWidget(clearSelectionBtn)

        layout = QVBoxLayout(self)
        layout.addWidget(label)
        layout.addLayout(buttonLayout)
        layout.addWidget(self.list)
        layout.addWidget(button)

        self.setLayout(layout)

    def restoreNotes(self) -> None:
        for item in self.list.selectedItems():
            nid, mid, fields = item.text().split("\t", 2)

            if mw.col.db.list("select id from notes where id = ?", nid):
                continue

            model = mw.col.models.get(nid)
            if model is None:
                continue

            note = Note(mw.col, model)
            note.fields = fields
            # add custom tag(s)

            cardCount = mw.col.addNote(note)
            if cardCount > 0:
                mw.col.db.execute("update Cards set nid = ? where nid = ?", nid, note.id)
                mw.col.db.execute("update Notes set id = ? where id = ?", nid, note.id)
            else:
                note.tags.append("no-card")
                note.flush()

    def onSelectAllClicked(self) -> None:
        self.list.selectAll()

    def onSelectNoneClicked(self) -> None:
        self.list.clearSelection()

    def onUndeleteButtonClicked(self) -> None:
        self.restoreNotes()

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
