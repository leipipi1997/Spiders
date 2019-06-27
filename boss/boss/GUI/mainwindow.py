import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from boss.GUI import loginwindow
from boss.GUI.chartViewwindow import showView

(form_class, qtbase_class) = uic.loadUiType('mainWindow.ui')


class MainWindow(qtbase_class, form_class):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(400, 300)
        self.queryDataButton.clicked.connect(lambda: self.add_function("queryData"))
        self.chartViewButton.clicked.connect(lambda: self.add_function("chartView"))
        self.exitButton.clicked.connect(lambda: self.add_function("exit"))

    def add_function(self, operate):
        if operate == "queryData":
            self.setVisible(0)
            from boss.GUI.queryDatawindow import QueryDataWindow                # 防止交叉引用导致错误
            QueryDataWindow().show()
            self.close()
        elif operate == "chartView":
            showView()
        elif operate == "exit":
            self.setVisible(0)
            loginwindow.LoginWindow().show()
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
