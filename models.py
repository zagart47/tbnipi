import numpy as np
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtGui import QColor


# Класс для создания пользовательской модели таблицы.
class CustomTableModel(QAbstractTableModel):
    def __init__(self, data):
        super(CustomTableModel, self).__init__()
        self._data = data

    # Возвращает число строк из таблицы
    def rowCount(self, parent=QModelIndex()):
        return self._data.shape[0]

    # Возвращает число столбцов из таблицы
    def columnCount(self, parent=QModelIndex()):
        return self._data.shape[1]

    # Позволяет корректно редактировать и отображать данные в таблцие и настраивает цвет ячеек
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self._data[index.row(), index.column()])
        elif role == Qt.BackgroundRole and index.column() == 3:
            value = self._data[index.row(), index.column()]
            if value > 0:
                return QColor(Qt.green)
            elif value < 0:
                return QColor(Qt.red)
        return None

    # Производит рассчеты во втором и третьем столбце таблицы
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self._data[index.row(), index.column()] = int(value)
            if index.column() == 0:
                self._data[:, 1] = np.cumsum(self._data[:, 0])
                self._data[:, 2] = self._data[:, 0] + self._data[:, 1] + 3
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    # Настраивает флаги для столбцов. Только первый может редактироваться.
    def flags(self, index):
        flags = super(CustomTableModel, self).flags(index)
        if index.column() == 0:
            flags |= Qt.ItemIsEditable
        return flags

    # Устанавливает заголовки для столбцов
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            headers = ["rand+CombBox", "cumsum", "c1+c2+3", "rand"]
            return headers[section]
        return super().headerData(section, orientation, role)

    # Обновляет таблицу.
    # Начинает сброс модели, обновляет внутренние данные и завершает сброс модели,
    # чтобы представление могло корректно отобразить новые данные.
    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()
