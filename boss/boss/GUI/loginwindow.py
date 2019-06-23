import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from ..DB import dataBase


(form_class, qtbase_class) = uic.loadUiType('loginWindow.ui')


class Loginwindow(qtbase_class, form_class):
    def __init__(self):
        super(Loginwindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(600, 300)
        self.signUpButton.clicked.connect(lambda:self.addfunction("signUp"))
        self.signInButton.clicked.connect(lambda:self.addfunction("signIn"))
        self.passwordLine.setEchoMode(QLineEdit.Password)
        # 连接数据库
        self.connect = dataBase.getConnect()
        # 通过cursor执行增删查改
        self.cursor = dataBase.getCursor(self.connect)

    def addfunction(self, operate):
        username = self.userNameLine.text()
        password = self.passwordLine.text()
        if len(username.strip()) == 0:
            QMessageBox.question(self, 'Tips', 'You did not enter a username!',QMessageBox.Yes)
        elif len(password.strip()) == 0:
            QMessageBox.question(self, 'Tips', 'You did not enter a password!',QMessageBox.Yes)
        else:
            self.connect.connect()
            try:
                sql = 'select * from user_info where userName = %s' % username
                self.cursor.execute(sql)
                # 提交sql语句
                result = self.cursor.fetchall()
                if operate == "signUp":
                    if len(result) != 0:
                        QMessageBox.question(self, 'Tips', 'username already exists!', QMessageBox.Yes)
                    else:
                        sql = "insert into user_info (userName, password) VALUE (%s, %s)"
                        data = (username, password)
                        self.cursor.execute(sql, data)
                        self.connect.commit()
                        QMessageBox.question(self, 'Tips', 'signUp successfully!', QMessageBox.Yes)
                elif operate == "signIn":
                    if len(result) == 0:
                        QMessageBox.question(self, 'Tips', 'You enter a wrong username!', QMessageBox.Yes)
                    elif result[0][1] != password:
                        QMessageBox.question(self, 'Tips', 'You enter a wrong password!', QMessageBox.Yes)
                    else:
                        self.setVisible(0)
                        from boss.GUI.mainwindow import Mainwindow
                        Mainwindow().show()
                        self.close()
            except:
                self.connect.rollback()
                self.connect.commit()  # 出错要回滚，回滚后一定要记得提交
            finally:
                self.connect.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Loginwindow()
    ui.show()
    sys.exit(app.exec_())