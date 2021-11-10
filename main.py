from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
import sqlite3
import sys

# соединение
conn = sqlite3.connect('todo.db')
# курсор
cur = conn.cursor()
# создание таблицы
cur.execute('CREATE TABLE if not exists todo_list(list_item text)')
# добавление изменений
conn.commit()
# завершение соединения
conn.close()


class To_Do(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 339)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.add_item_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add_item())
        self.save_all_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.save_all_items())
        self.delete_item_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete_item())
        self.clear_items_pushButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.clear_item())
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.add_item_pushButton.setObjectName("add_item_pushButton")
        self.save_all_pushButton.setObjectName("save_all_pushButton")
        self.delete_item_pushButton.setObjectName("delete_item_pushButton")
        self.clear_items_pushButton.setObjectName("clear_items_pushButton")
        self.listWidget.setObjectName("listWidget")
        # геометрия виджетов
        self.lineEdit.setGeometry(QtCore.QRect(10, 10, 470, 31))
        self.add_item_pushButton.setGeometry(QtCore.QRect(10, 50, 111, 31))
        self.save_all_pushButton.setGeometry(QtCore.QRect(130, 50, 111, 31))
        self.delete_item_pushButton.setGeometry(QtCore.QRect(250, 50, 111, 31))
        self.clear_items_pushButton.setGeometry(QtCore.QRect(370, 50, 111, 31))
        self.listWidget.setGeometry(QtCore.QRect(10, 90, 470, 241))

        _translate = QtCore.QCoreApplication.translate

        # текст
        MainWindow.setWindowTitle(_translate("MainWindow", "To Do List "))
        self.add_item_pushButton.setText(_translate("MainWindow", "Add Task"))
        self.save_all_pushButton.setText(_translate("MainWindow", "Save Tasks"))
        self.delete_item_pushButton.setToolTip(_translate("MainWindow", "Delete Task"))
        self.clear_items_pushButton.setText(_translate("MainWindow", "Clear Tasks"))
        # шрифт
        self.lineEdit.setFont(QFont('times', 8))
        self.add_item_pushButton.setFont(QFont('times', 8))
        self.save_all_pushButton.setFont(QFont('Ariel', 8))
        self.delete_item_pushButton.setFont(QFont('times', 8))
        self.clear_items_pushButton.setFont(QFont('times', 8))
        self.listWidget.setFont(QFont('times', 8))
        # кнопки
        self.lineEdit.setToolTip(_translate("MainWindow", "Enter Task"))
        self.add_item_pushButton.setToolTip(_translate("MainWindow", "Add Task"))
        self.save_all_pushButton.setToolTip(_translate("MainWindow", "Save all Tasks"))
        self.delete_item_pushButton.setText(_translate("MainWindow", "Delete Task"))
        self.clear_items_pushButton.setToolTip(_translate("MainWindow", "Clear Tasks"))

        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter Task"))

        self.get_items()

    def get_items(self):

        conn = sqlite3.connect('todo.db')

        cur = conn.cursor()

        cur.execute('SELECT * FROM todo_list')

        rows = cur.fetchall()

        conn.commit()

        conn.close()
        # итерация по каждой строке
        for row in rows:
            # add data in list
            self.listWidget.addItem(str(row[0]))

    def add_item(self):

        # получение введенного элемента
        item = self.lineEdit.text()
        # добавление элемента
        self.listWidget.addItem(item)
        # очистить запись элемента
        item = self.lineEdit.setText("")

    def save_all_items(self):

        conn = sqlite3.connect('todo.db')

        cur = conn.cursor()

        cur.execute('DELETE FROM todo_list')

        items = []
        # итерация элементов виджета
        for i in range(self.listWidget.count()):
            # добавление элемента
            items.append(self.listWidget.item(i))

        for item in items:
            # вставление элементов в таблицу
            cur.execute("INSERT INTO todo_list VALUES (:item)", {'item': item.text()})

        conn.commit()

        conn.close()

    def delete_item(self):
        # получение номера элемента
        clicked = self.listWidget.currentRow()
        # удаление
        self.listWidget.takeItem(clicked)

    def clear_item(self):

        self.listWidget.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = To_Do()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())