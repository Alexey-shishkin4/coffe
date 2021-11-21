import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QApplication, QTableWidgetItem

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('espresso')
        self.con = sqlite3.connect('coffee.sqlite')
        self.pushButton.clicked.connect(self.update_result)
        self.update_result()
    

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM cof").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            return
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = ['ИД', 'Название', 'Обжарка', 'Тип', 'Вкус', 'Цена(р)', 'Размер(г)']
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())