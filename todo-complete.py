import json
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

# Import UI FILE
from MainWindow import Ui_MainWindow

tick = QtGui.QImage("tick.png")
cross = QtGui.QImage("cross.png")


class TodoModel(QtCore.QAbstractListModel):
   def __init__(self, todos=None):
      super().__init__()
      self.todos = todos or []
   
   def data(self, index, role):
      if role == Qt.DisplayRole:
         _, text = self.todos[index.row()]
         return text

      if role == Qt.DecorationRole:
         status, _ = self.todos[index.row()]
         if status:
            return tick
         else:
            return cross
         
   def rowCount(self, index):
      return len(self.todos)
   

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
   def __init__(self):
      super().__init__()
      
      # Setting a Window Icon
      self.setWindowIcon(QtGui.QIcon("icon.png"))
      # Setting Minimum Size
      self.setMinimumSize(600,600)
   
      self.setupUi(self)
      self.model = TodoModel()
      self.load()
      self.todoView.setModel(self.model)
      
      self.addButton.pressed.connect(self.add)
      # Creating ENTER Key Shortcut to a lineEdit to add tasks
      self.todoEdit.returnPressed.connect(self.add)

      self.deleteButton.pressed.connect(self.delete)
      self.del_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Delete),self)
      self.del_shortcut.activated.connect(self.delete)
      
      self.completeButton.pressed.connect(self.complete)
      self.complete_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+D"),self)
      self.complete_shortcut.activated.connect(self.complete)
      
   def add(self):
      text = self.todoEdit.text()
      if text:
         self.model.todos.append((False, text))
         self.model.layoutChanged.emit()
         self.todoEdit.setText("")
         self.save()
         
   
   def delete(self):
      indexes = self.todoView.selectedIndexes()
      if indexes:
         index = indexes[0]
         del self.model.todos[index.row()]
         self.model.layoutChanged.emit()
         self.todoView.clearSelection()
         self.save()
   
   def complete(self):
      indexes = self.todoView.selectedIndexes()
      if indexes:
         index = indexes[0]
         row = index.row()
         status, text = self.model.todos[row]
         self.model.todos[row] = (True, text)
         self.model.layoutChanged.emit()
         self.model.dataChanged.emit(index, index)
         self.todoView.clearSelection()
         self.save()
   
   def load(self):
      try:
         with open("data.json","r") as f:
            self.model.todos = json.load(f)
      except Exception:
         pass
   
   def save(self):
      with open("data.json","w") as f:
         data = json.dump(self.model.todos, f)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()