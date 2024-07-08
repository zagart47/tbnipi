from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox


# Класс для создания делегата с выпадающим списком.
class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = [str(i) for i in range(1, 6)]

    # Создает выпадающий список, добавляет элементы в этот список и создает сигнал об изменении текста
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        editor.addItems(self.items)
        editor.currentTextChanged.connect(
            lambda text: self.commitData.emit(editor))
        return editor

    # Получает текущее значение ячейки и помещает его в ComboBox
    def setEditorData(self, editor, index):
        value = index.data(Qt.EditRole)
        if value is not None:
            editor.setCurrentText(value)

    # Получает текущий текст из ComboBox, устанавливает его в модель данных и сигнализирует об этом
    def setModelData(self, editor, model, index):
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)
        self.commitData.emit(editor)

    # Обновляет геометрию редактора, чтобы ComboBox корректно отображался в ячейке таблицы
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
