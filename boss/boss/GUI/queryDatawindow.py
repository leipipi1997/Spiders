import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from boss.GUI.queryData import queryData
from boss.GUI import mainwindow

(form_class, qtbase_class) = uic.loadUiType('queryDatawindow.ui')

class QueryDatawindow(qtbase_class, form_class):
    def __init__(self):
        super(QueryDatawindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(650, 400)
        self.resultTableWidget.verticalHeader().setHidden(True)
        self.comfireButton.clicked.connect(lambda: self.addFunction("comfire"))
        self.exitButton.clicked.connect(lambda: self.addFunction("exit"))

    def addFunction(self, operate):
        if operate == "comfire":
            selectedCity = self.cityBox.currentText()
            selectedSalary = self.salaryBox.currentText()
            selectedWorkYear = self.workYearBox.currentText()
            selectedEducation = self.educationBox.currentText()
            result = queryData(selectedCity, selectedSalary, selectedWorkYear, selectedEducation)
            if result[0] == "No such a job!":
                QMessageBox.question(self, 'Tips', 'No such a job!', QMessageBox.Yes)
            else:
                rowCount = self.resultTableWidget.rowCount()
                for i in range(rowCount):
                    self.resultTableWidget.removeRow(0)
                for i in result:
                    rowCount = self.resultTableWidget.rowCount()
                    self.resultTableWidget.insertRow(rowCount)
                    self.resultTableWidget.setItem(rowCount, 0, QTableWidgetItem(i[0]))
                    self.resultTableWidget.setItem(rowCount, 1, QTableWidgetItem(i[1]))
                    self.resultTableWidget.setItem(rowCount, 2, QTableWidgetItem(i[2]))
                    self.resultTableWidget.setItem(rowCount, 3, QTableWidgetItem(i[3]))
                    self.resultTableWidget.setItem(rowCount, 4, QTableWidgetItem(i[4]))
                    self.resultTableWidget.setItem(rowCount, 5, QTableWidgetItem(i[5]))
                    self.resultTableWidget.setItem(rowCount, 6, QTableWidgetItem(i[6]))
                    self.resultTableWidget.setItem(rowCount, 7, QTableWidgetItem(i[7]))
                    self.resultTableWidget.setItem(rowCount, 8, QTableWidgetItem(i[8]))
                    self.resultTableWidget.setItem(rowCount, 9, QTableWidgetItem(i[9]))
        elif operate == "exit":
            self.setVisible(0)
            mainwindow.Mainwindow().show()
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = QueryDatawindow()
    ui.show()
    sys.exit(app.exec_())