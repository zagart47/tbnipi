import numpy as np
import h5py
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QInputDialog, QFileDialog
import pyqtgraph as pg
from scipy.stats import linregress

from delegates import ComboBoxDelegate
from models import CustomTableModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Программа")
        self.setGeometry(0, 0, 1920, 1000)

        self.data = np.zeros((10, 4), dtype=int)
        self.data[:, 0] = np.random.randint(-5, 11, size=10)
        self.data[:, 3] = np.random.randint(-5, 11, size=10)

        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.table_view = QTableView()
        self.model = CustomTableModel(self.data)
        self.table_view.setModel(self.model)
        self.table_view.setItemDelegateForColumn(0, ComboBoxDelegate())
        self.model.dataChanged.connect(self.update_table)
        main_layout.addWidget(self.table_view)

        button_layout = QHBoxLayout()

        self.resize_button = QPushButton("Изменить размер таблицы")
        self.resize_button.clicked.connect(self.resize_table)
        button_layout.addWidget(self.resize_button)

        self.randomize_button = QPushButton("Рандомизировать значения")
        self.randomize_button.clicked.connect(self.randomize_values)
        button_layout.addWidget(self.randomize_button)

        self.save_button = QPushButton("Сохранить данные")
        self.save_button.clicked.connect(self.save_data)
        button_layout.addWidget(self.save_button)

        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_data)
        button_layout.addWidget(self.load_button)

        main_layout.addLayout(button_layout)

        self.plot_widget = pg.PlotWidget()  # Добавляем график в макет
        self.plot_widget.setBackground('w')
        main_layout.addWidget(self.plot_widget)

        self.table_view.selectionModel().selectionChanged.connect(
            self.update_plot)

        self.update_table(self.model.index(0, 0))

    def update_table(self, top_left):
        # Обновляет 2 и 3 столбцы в таблице и сигнализирует об этом
        if top_left.column() == 0:
            self.data[:, 1] = np.cumsum(self.data[:, 0])
            self.data[:, 2] = self.data[:, 0] + self.data[:, 1] + 3
            self.model.dataChanged.emit(self.model.index(0, 1), self.model.index(self.data.shape[0] - 1, 2),
                                        [Qt.DisplayRole])

    def update_plot(self):
        # Формирует график
        selected_columns = list(
            index.column() for index in self.table_view.selectedIndexes())
        selected_columns = self.remove_duplicates(selected_columns)
        self.plot_widget.clear()
        if len(selected_columns) == 2:
            x_col = selected_columns[0]
            y_col = selected_columns[1]
            x = self.data[:, x_col]
            y = self.data[:, y_col]
            self.plot_widget.clear()

            self.plot_widget.plot(x, y, pen='b', symbol='d')  # Рисует график

            slope, intercept, r_value, p_value, std_err = linregress(x, y)  # scipy вычисляет линейную регрессию
            fit_x = np.array([min(x), max(x)])
            fit_y = slope * fit_x + intercept

            self.plot_widget.plot(fit_x, fit_y, pen='r')  # Добавляем линейную регрессию на график

            x_label = self.model.headerData(x_col, Qt.Horizontal, Qt.DisplayRole)
            y_label = self.model.headerData(y_col, Qt.Horizontal, Qt.DisplayRole)
            self.plot_widget.setLabel('bottom', x_label)  # Добавляем подписи осей
            self.plot_widget.setLabel('left', y_label)  # Добавляем подписи осей

    def remove_duplicates(self, nested_list):
        # Удаляет дубликаты индексов выделенных столбцов. Как по-другому сделать пока не понял
        unique_list = []
        seen = set()
        for element in nested_list:
            if element not in seen:
                unique_list.append(element)
                seen.add(element)
        return unique_list

    def resize_table(self):
        # Меняет размер таблицы
        rows, ok = QInputDialog.getInt(self, "Изменить размер таблицы", "Число строк:", self.data.shape[0], 1, 100)
        if ok:
            self.table_view.clearSelection()
            new_data = np.zeros((rows, 4), dtype=int)
            new_data[:min(self.data.shape[0], rows), :] = self.data[:min(self.data.shape[0], rows), :]

            if rows > self.data.shape[0]:
                new_rows = rows - self.data.shape[0]
                new_data[-new_rows:, 0] = np.random.randint(-5, 11, size=new_rows)
                new_data[-new_rows:, 3] = np.random.randint(-5, 11, size=new_rows)

            self.data = new_data
            self.model.update_data(self.data)
            self.update_table(self.model.index(0, 0))

    def randomize_values(self):
        # Заполняет ячейки столбцо 1 и 4 случайными значениями от [-5 до 10]
        self.table_view.clearSelection()
        self.data[:, 0] = np.random.randint(-5, 11, size=self.data.shape[0])
        self.data[:, 3] = np.random.randint(-5, 11, size=self.data.shape[0])
        self.update_table(self.model.index(0, 0))
        self.model.dataChanged.emit(self.model.index(0, 0), self.model.index(self.data.shape[0] - 1, 3),
                                    [Qt.DisplayRole])

    def save_data(self):
        # Сохраняет данные таблицы в hdf файл
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить данные", "", "HDF5 Files (*.h5);;All Files (*)",
                                                   options=options)
        if file_name:
            with h5py.File(file_name, 'w') as f:
                f.create_dataset('column_1', data=self.data[:, 0])
                f.create_dataset('column_4', data=self.data[:, 3])

    def load_data(self):
        # Загружает данные из hdf файла, подгоняет размер таблицы в модели и заменяет данные в таблице
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить данные", "", "HDF5 Files (*.h5);;All Files (*)",
                                                   options=options)
        if file_name:
            with h5py.File(file_name, 'r') as f:
                column_1 = f['column_1'][:]
                column_4 = f['column_4'][:]

                new_data = np.zeros((len(column_1), 4), dtype=int)
                new_data[:, 0] = column_1
                new_data[:, 3] = column_4

                self.data = new_data
                self.model.update_data(self.data)

                self.data[:, 1] = np.cumsum(self.data[:, 0])
                self.data[:, 2] = self.data[:, 0] + self.data[:, 1] + 3
                self.model.update_data(self.data)
                self.update_table(self.model.index(0, 0))
