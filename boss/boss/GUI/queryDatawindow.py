import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem
from boss.GUI.queryData import query_data
from boss.GUI import mainwindow

(form_class, qtbase_class) = uic.loadUiType('queryDatawindow.ui')


class QueryDataWindow(qtbase_class, form_class):
    def __init__(self):
        super(QueryDataWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(650, 400)
        self.resultTableWidget.verticalHeader().setHidden(True)
        self.comfireButton.clicked.connect(lambda: self.add_function("comfire"))
        self.exitButton.clicked.connect(lambda: self.add_function("exit"))

    def add_function(self, operate):
        if operate == "comfire":
            selected_city = self.cityBox.currentText()
            selected_salary = self.salaryBox.currentText()
            selected_work_year = self.workYearBox.currentText()
            selected_education = self.educationBox.currentText()
            result = query_data(selected_city, selected_salary, selected_work_year, selected_education)

            if result[0] == "No such a job!":
                QMessageBox.question(self, 'Tips', 'No such a job!', QMessageBox.Yes)
            else:
                row_count = self.resultTableWidget.rowCount()
                for i in range(row_count):
                    self.resultTableWidget.removeRow(0)
                for i in result:
                    row_count = self.resultTableWidget.rowCount()
                    self.resultTableWidget.insertRow(row_count)
                    self.resultTableWidget.setItem(row_count, 0, QTableWidgetItem(i[0]))
                    self.resultTableWidget.setItem(row_count, 1, QTableWidgetItem(i[1]))
                    self.resultTableWidget.setItem(row_count, 2, QTableWidgetItem(i[2]))
                    self.resultTableWidget.setItem(row_count, 3, QTableWidgetItem(i[3]))
                    self.resultTableWidget.setItem(row_count, 4, QTableWidgetItem(i[4]))
                    self.resultTableWidget.setItem(row_count, 5, QTableWidgetItem(i[5]))
                    self.resultTableWidget.setItem(row_count, 6, QTableWidgetItem(i[6]))
                    self.resultTableWidget.setItem(row_count, 7, QTableWidgetItem(i[7]))
                    self.resultTableWidget.setItem(row_count, 8, QTableWidgetItem(i[8]))
                    self.resultTableWidget.setItem(row_count, 9, QTableWidgetItem(i[9]))
        elif operate == "exit":
            self.setVisible(0)
            mainwindow.MainWindow().show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = QueryDataWindow()
    ui.show()
    sys.exit(app.exec_())
