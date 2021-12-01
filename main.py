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
        self.pushButton_3.clicked.connect(self.open_second_form)
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
    
    def open_second_form(self):
        self.second_form = SecondForm(self, "Данные для второй формы")
        self.second_form.show()

class SecondForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.setWindowTitle('espresso')
        self.pushButton.clicked.connect(self.update_table)
    
    def update_table(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if len(self.lineEdit.text()) > 0:
            if all([self.lineEdit_2.text(), self.lineEdit_3.text(), self.lineEdit_4.text(), self.lineEdit_5.text(), self.lineEdit_6.text()]):
                cur.execute(f'''INSERT INTO cof(name, objarka, type, vkus, price, size) VALUES
                ('{self.lineEdit.text()}', '{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}',
                '{self.lineEdit_4.text()}', '{self.lineEdit_5.text()}', '{self.lineEdit_6.text()}')''')
                con.commit()
        if self.lineEdit_7.text():
            sp = [(self.lineEdit_11.text(), 'name'), (self.lineEdit_13.text(), 'objarka'),
                  (self.lineEdit_10.text(), 'type'), (self.lineEdit_12.text(), 'vkus'),
                  (self.lineEdit_8.text(), 'price'), (self.lineEdit_9.text(), 'size')]
            self.modified = {}
            for i in sp:
                if not i[0]:
                    self.modified[i[1]] = cur.execute(f'''select {i[1]} from cof where id = {self.lineEdit_7.text()}''').fetchall()[0][0]
                else:
                    self.modified[i[1]] = i[0]
            que = "UPDATE cof SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += f" WHERE id = {self.lineEdit_7.text()}"
            cur.execute(que)
            con.commit()
            self.modified.clear()
                




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())