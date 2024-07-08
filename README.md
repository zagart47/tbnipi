![Static Badge](https://img.shields.io/badge/%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81-%D0%B3%D0%BE%D1%82%D0%BE%D0%B2-blue)
![Static Badge](https://img.shields.io/badge/Python-3.8-green)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/zagart47/tbnipi)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/zagart47/tbnipi)
![GitHub forks](https://img.shields.io/github/forks/zagart47/tbnipi)

# tbnipi
Десктопное приложение разработанное в рамках тестового задания

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Разработка](#разработка)
- [Contributing](#contributing)
- [FAQ](#faq)
- [To do](#to-do)
- [Команда проекта](#команда-проекта)

## Технологии
- [Python](https://www.python.org/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [NumPy](https://numpy.org)
- [SciPy](https://scipy.org/)
- [PyQtGraph](https://www.pyqtgraph.org/)

## Использование
```powershell
pip install requirements.txt
python main.py
```

## Разработка

### Требования
Для установки и запуска проекта необходимы python версии 3.8 и прямые руки.

## Contributing
Если у вас есть предложения или идеи по дополнению проекта или вы нашли ошибку, то пишите мне в tg: @zagart47

## FAQ
### Зачем ты разработал этот проект?
Это тестовое задание.

## To do
- [x] Окно должно содержать таблицу (QTableView) с числами и график под таблицей.
- [x] Все данные внутри должны храниться в двумерном numpy-массиве.
- [x] Один из столбцов таблицы должен позволять редактировать числа только из выпадающего списка чисел от 1 до 5.
- [x] Значения в одном из столбцов должны пересчитываться из значений в этой же строчке в другом столбце. Должен быть сигнал, на который все могут подписаться.
- [x] Значения в одном из столбцов должны содержать накопленные значения из другого столбца. Должен быть сигнал, на который все могут подписаться.
- [x] При выборе двух столбцов должен отображаться график (желательно в pyqtgraph) зависимости второго выбранного столбца от первого.
- [x] Нужны кнопки для сохранения массива в текстовый файл или в hdf, загрузки его из текстового файла или hdf, для изменения размера массива и заполнения его (кроме особенных ячеек, которые пересчитываются) случайными значениями.
- [x]  В одном из столбцов ячейки должны заливаться красным или зеленым цветом в зависимости от того, положительные они или отрицательные.
- [x] Факультативно: Второй вариант той же самой программы - когда данные внутри не хранятся в промежуточном numpy-массиве, и работа идет непосредственно с датасетом из hdf-файла БЕЗ кеширования из пункта 2.
- [x] Плюсом будет, если код будет прокомментирован (при этом комментарии должны описывать, что и зачем происходит, а не как).

## Команда проекта
- [Артур Загиров](https://t.me/zagart47) — Developer
