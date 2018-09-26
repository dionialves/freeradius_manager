
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QTableWidgetItem, QAbstractItemView,
                             QHeaderView, QDialog, QMessageBox)

from views.management_freeradius import Ui_MainWindow
from models.freeradius import FreeRadius
from views.update_register import Ui_Dialog
from views.create_register import Ui_FormCreateRegister


class CreateRegister(QDialog):
    def __init__(self):
        super(CreateRegister, self).__init__()
        self.ui = Ui_FormCreateRegister()
        self.ui.setupUi(self)

        self.ui.label_message.setStyleSheet("color: rgb(255, 0, 0);")
        self.ui.label_message.setFont(QFont("MS Shell Dlg 2", 8, QFont.Normal))


class UpdateRegister(QDialog):
    def __init__(self):
        super(UpdateRegister, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def set_username(self, username):
        self.ui.lineEdit_username.setText(username)

    def set_attribute(self, attribute):
        self.ui.lineEdit_attribute.setText(attribute)

    def set_operation(self, operation):
        self.ui.lineEdit_operation.setText(operation)

    def set_value(self, value):
        self.ui.lineEdit_value.setText(value)


class MainWindow(QMainWindow, FreeRadius):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.label_message.setStyleSheet("color: rgb(255, 0, 0);")
        self.ui.label_message.setFont(QFont("MS Shell Dlg 2", 8, QFont.Normal))

        self.ui.btn_search.clicked.connect(self.search_user)
        self.ui.lineEdit_search.returnPressed.connect(lambda: self.search_user())
        self.create_table()

        self.form_update = UpdateRegister()
        self.ui.btn_update.clicked.connect(self.view_update_register)
        self.ui.table.doubleClicked.connect(self.view_update_register)
        self.form_update.ui.btn_save.clicked.connect(self.update_register)

        self.form_create = CreateRegister()
        self.ui.btn_create.clicked.connect(self.view_create_register)
        self.form_create.ui.btn_save.clicked.connect(self.create_register)

        self.ui.btn_delete.clicked.connect(self.view_delete_register)

        self.form_create.ui.btn_cancel.clicked.connect(self.form_create.close)
        self.form_update.ui.btn_cancel.clicked.connect(self.form_update.close)

        self.ui.actionSair.triggered.connect(self.close)
        self.ui.btn_close.clicked.connect(self.close)

    def view_delete_register(self):
        if self.ui.table.currentItem():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText("Você tem certeza que deseja excluir esse registro?")
            msg.setWindowTitle("Tem certeza que deseja excluir?")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            ret = msg.exec_()
            if ret == QMessageBox.Ok:
                self.delete_register()

    def delete_register(self):
        row = self.ui.table.currentItem().row()
        model = self.ui.table.model()

        pk = model.index(row, 0)
        pk = str(model.data(pk))
        attribute = model.index(row, 2)
        attribute = str(model.data(attribute))
        if attribute == 'User-Password':
            table = 'radcheck'
        else:
            table = 'radreply'

        self.delete_pk(pk, table)
        self.search_user()

    def view_update_register(self):
        if self.ui.table.currentItem():
            row = self.ui.table.currentItem().row()
            model = self.ui.table.model()

            data_line = []
            for x in range(5):
                index = model.index(row, x)
                data_line.append(str(model.data(index)))

            self.form_update.set_username(data_line[1])
            self.form_update.set_attribute(data_line[2])
            self.form_update.set_operation(data_line[3])
            self.form_update.set_value(data_line[4])
            self.form_update.exec_()

    def update_register(self):
        if self.form_update.ui.lineEdit_attribute.text() == 'Mikrotik-Rate-Limit':
            speed = self.form_update.ui.lineEdit_value.text().split('/')
            self.update_speed_control(self.form_update.ui.lineEdit_username.text(),
                                                 speed[0].replace('k', ''),
                                                 speed[1].replace('k', ''))

        elif self.form_update.ui.lineEdit_attribute.text() == 'User-Password':
            self.update_user(self.form_update.ui.lineEdit_username.text(), self.form_update.ui.lineEdit_value.text())
        elif self.form_update.ui.lineEdit_attribute.text() == 'Framed-IP-Address':
            self.update_ip(self.form_update.ui.lineEdit_username.text(), self.form_update.ui.lineEdit_value.text())

        self.form_update.close()
        self.search_user()

    def view_create_register(self):
        self.form_create.ui.lineEdit_username.setText("")
        self.form_create.ui.lineEdit_value.setText("")
        self.form_create.ui.label_message.setText("")

        self.form_create.exec_()

    def create_register(self):
        username = self.form_create.ui.lineEdit_username.text()
        attribute = self.form_create.ui.comboBox_attribute.currentText()
        operation = self.form_create.ui.comboBox_operation.currentText()
        value = self.form_create.ui.lineEdit_value.text()

        if username and attribute and operation and value:
            if attribute == 'Mikrotik-Rate-Limit':
                speed = self.form_create.ui.lineEdit_value.text().split('/')
                self.add_speed_control(username, speed[0].replace('k', ''), speed[1].replace('k', ''))
            elif attribute == 'User-Password':
                self.add_user(username, value)
            elif attribute == 'Framed-IP-Address':
                self.add_ip(username, value)

            self.ui.lineEdit_search.setText(username)
            self.form_create.close()
            self.search_user()
        else:
            self.form_create.ui.label_message.setText("Você precisa preencher todos os campos")

    def create_table(self):
        self.ui.table.setColumnCount(5)
        self.ui.table.setHorizontalHeaderLabels(('id', 'username', 'attribute', 'op', 'value'))
        self.ui.table.verticalHeader().hide()
        self.ui.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        header = self.ui.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        self.ui.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def insert_data_in_table(self, data):
        if data:
            self.ui.table.setRowCount(len(data[:20]))
            count_row = 0
            for x in data[:20]:
                self.ui.table.setItem(count_row, 0, QTableWidgetItem(str(x[0])))
                self.ui.table.setItem(count_row, 1, QTableWidgetItem(x[1]))
                self.ui.table.setItem(count_row, 2, QTableWidgetItem(x[2]))
                self.ui.table.setItem(count_row, 3, QTableWidgetItem(x[3]))
                self.ui.table.setItem(count_row, 4, QTableWidgetItem(x[4]))
                count_row += 1
        else:
            self.ui.table.setRowCount(0)

    def search_of_record_in_the_database(self, user):
        data = []
        if self.connect != -1:
            sql = """SELECT id, username, attribute, op, value FROM radreply WHERE username LIKE '%{}%'
                     UNION ALL
                     SELECT id, username, attribute, op, value FROM radcheck WHERE username LIKE '%{}%';""".format(user, user)

            self.connect.execute(sql)
            data = self.connect.fetchall()

        return data

    def search_user(self):
        data_of_database = self.search_of_record_in_the_database(self.ui.lineEdit_search.text())
        self.insert_data_in_table(data_of_database)