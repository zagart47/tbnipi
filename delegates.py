from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox


class ComboBoxDelegate(QStyledItemDelegate):
    """
    Класс для создания делегата с выпадающим списком.
    """
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)

        self.items = [str(i) for i in range(1, 6)]  # Инициализация списка элементов для выпадающего списка

    def createEditor(self, parent, option, index):
        """
        Создает выпадающий список, добавляет элементы в этот список и создает сигнал об изменении текста
        """
        editor = QComboBox(parent)
        editor.addItems(self.items)
        editor.currentTextChanged.connect(lambda text: self.commitData.emit(editor))
        return editor

    def setEditorData(self, editor, index):
        """
        Получает текущее значение ячейки и помещает его в ComboBox
        """
        value = index.data(Qt.EditRole)
        if value is not None:
            editor.setCurrentText(value)

    def setModelData(self, editor, model, index):
        """
        Получает текущий текст из ComboBox, устанавливает его в модель данных и сигнализирует об этом
        """
        value = editor.currentText()
        model.setData(index, value, Qt.EditRole)

        self.commitData.emit(editor)

    def updateEditorGeometry(self, editor, option, index):
        """
        Обновляет геометрию редактора, чтобы ComboBox корректно отображался в ячейке таблицы
        """
        editor.setGeometry(option.rect)
