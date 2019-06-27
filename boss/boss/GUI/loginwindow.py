import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QLineEdit
from boss.DB import DBPool


(form_class, qtbase_class) = uic.loadUiType('loginWindow.ui')


class LoginWindow(qtbase_class, form_class):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.pool = DBPool.MySqlPool()
        self.setupUi(self)
        self.setFixedSize(600, 300)
        self.signUpButton.clicked.connect(lambda: self.add_function("signUp"))
        self.signInButton.clicked.connect(lambda: self.add_function("signIn"))
        self.passwordLine.setEchoMode(QLineEdit.Password)

    def add_function(self, operate):
        username = self.userNameLine.text()
        password = self.passwordLine.text()
        if len(username.strip()) == 0:
            QMessageBox.question(self, 'Tips', 'You did not enter a username!', QMessageBox.Yes)
        elif len(password.strip()) == 0:
            QMessageBox.question(self, 'Tips', 'You did not enter a password!', QMessageBox.Yes)
        else:
            self.pool.get_conn()
            sql = 'select * from user_info where userName = %s' % username
            # 提交sql语句
            result = self.pool.query_(sql)
            if operate == "signUp":
                if len(result) != 0:
                    QMessageBox.question(self, 'Tips', 'username already exists!', QMessageBox.Yes)
                else:
                    sql = "insert into user_info (userName, password) VALUE (%s, %s)"
                    data = (username, password)
                    self.pool.insert_(sql, data)
                    self.pool.end()
                    QMessageBox.question(self, 'Tips', 'signUp successfully!', QMessageBox.Yes)
            elif operate == "signIn":
                if len(result) == 0:
                    QMessageBox.question(self, 'Tips', 'You enter a wrong username!', QMessageBox.Yes)
                elif result[0][1] != password:
                    QMessageBox.question(self, 'Tips', 'You enter a wrong password!', QMessageBox.Yes)
                else:
                    self.setVisible(0)
                    from boss.GUI.mainwindow import MainWindow
                    MainWindow().show()
                    self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = LoginWindow()
    ui.show()
    sys.exit(app.exec_())
