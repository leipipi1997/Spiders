import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from boss.GUI import loginwindow
from boss.GUI.chartViewwindow import showView

(form_class, qtbase_class) = uic.loadUiType('mainWindow.ui')

class Mainwindow(qtbase_class, form_class):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(400, 300)
        self.queryDataButton.clicked.connect(lambda: self.addFunction("queryData"))
        self.chartViewButton.clicked.connect(lambda: self.addFunction("chartView"))
        self.exitButton.clicked.connect(lambda: self.addFunction("exit"))

    def addFunction(self, operate):
        if operate == "queryData":
            self.setVisible(0)
            from boss.GUI.queryDatawindow import QueryDatawindow                #防止交叉引用导致错误
            QueryDatawindow().show()
            self.close()
        elif operate == "chartView":
            showView()
        elif operate == "exit":
            self.setVisible(0)
            loginwindow.Loginwindow().show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Mainwindow()
    ui.show()
    sys.exit(app.exec_())