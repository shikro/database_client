# Form implementation generated from reading ui file 'reader.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_reader_window(object):
    def setupUi(self, reader_window):
        reader_window.setObjectName("reader_window")
        reader_window.resize(700, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(reader_window.sizePolicy().hasHeightForWidth())
        reader_window.setSizePolicy(sizePolicy)
        reader_window.setMinimumSize(QtCore.QSize(700, 550))
        reader_window.setMaximumSize(QtCore.QSize(700, 550))
        self.centralwidget = QtWidgets.QWidget(reader_window)
        self.centralwidget.setObjectName("centralwidget")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setGeometry(QtCore.QRect(10, 10, 681, 531))
        self.toolBox.setObjectName("toolBox")
        self.library_page = QtWidgets.QWidget()
        self.library_page.setGeometry(QtCore.QRect(0, 0, 681, 429))
        self.library_page.setObjectName("library_page")
        self.tab_widget = QtWidgets.QTabWidget(self.library_page)
        self.tab_widget.setGeometry(QtCore.QRect(0, 0, 681, 431))
        self.tab_widget.setObjectName("tab_widget")
        self.order_statuses_tab = QtWidgets.QWidget()
        self.order_statuses_tab.setObjectName("order_statuses_tab")
        self.tab_widget.addTab(self.order_statuses_tab, "")
        self.create_order_tab = QtWidgets.QWidget()
        self.create_order_tab.setObjectName("create_order_tab")
        self.books_table = QtWidgets.QTableWidget(self.create_order_tab)
        self.books_table.setGeometry(QtCore.QRect(10, 10, 661, 251))
        self.books_table.setRowCount(0)
        self.books_table.setObjectName("books_table")
        self.books_table.setColumnCount(4)
        item = QtWidgets.QTableWidgetItem()
        self.books_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.books_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.books_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.books_table.setHorizontalHeaderItem(3, item)
        self.books_table.horizontalHeader().setDefaultSectionSize(160)
        self.books_table.horizontalHeader().setSortIndicatorShown(True)
        self.books_table.horizontalHeader().setStretchLastSection(False)
        self.books_in_order_list = QtWidgets.QListWidget(self.create_order_tab)
        self.books_in_order_list.setGeometry(QtCore.QRect(10, 290, 331, 101))
        self.books_in_order_list.setObjectName("books_in_order_list")
        self.create_order_button = QtWidgets.QPushButton(self.create_order_tab)
        self.create_order_button.setGeometry(QtCore.QRect(450, 330, 131, 51))
        self.create_order_button.setObjectName("create_order_button")
        self.return_date_edit = QtWidgets.QDateEdit(self.create_order_tab)
        self.return_date_edit.setGeometry(QtCore.QRect(510, 290, 110, 24))
        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setDate(QtCore.QDate(2022, 12, 1))
        self.return_date_edit.setObjectName("return_date_edit")
        self.label_5 = QtWidgets.QLabel(self.create_order_tab)
        self.label_5.setGeometry(QtCore.QRect(430, 290, 81, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.create_order_tab)
        self.label_6.setGeometry(QtCore.QRect(10, 270, 71, 16))
        self.label_6.setObjectName("label_6")
        self.tab_widget.addTab(self.create_order_tab, "")
        self.toolBox.addItem(self.library_page, "")
        self.events_page = QtWidgets.QWidget()
        self.events_page.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.events_page.setObjectName("events_page")
        self.toolBox.addItem(self.events_page, "")
        self.account_info_page = QtWidgets.QWidget()
        self.account_info_page.setGeometry(QtCore.QRect(0, 0, 681, 429))
        self.account_info_page.setObjectName("account_info_page")
        self.label = QtWidgets.QLabel(self.account_info_page)
        self.label.setGeometry(QtCore.QRect(20, 10, 60, 20))
        self.label.setObjectName("label")
        self.name_edit = QtWidgets.QLineEdit(self.account_info_page)
        self.name_edit.setGeometry(QtCore.QRect(90, 10, 261, 20))
        self.name_edit.setMaxLength(50)
        self.name_edit.setObjectName("name_edit")
        self.label_2 = QtWidgets.QLabel(self.account_info_page)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 60, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.account_info_page)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 60, 20))
        self.label_3.setObjectName("label_3")
        self.phone_edit = QtWidgets.QLineEdit(self.account_info_page)
        self.phone_edit.setGeometry(QtCore.QRect(90, 40, 261, 20))
        self.phone_edit.setMaxLength(20)
        self.phone_edit.setReadOnly(True)
        self.phone_edit.setObjectName("phone_edit")
        self.email_edit = QtWidgets.QLineEdit(self.account_info_page)
        self.email_edit.setGeometry(QtCore.QRect(90, 70, 261, 20))
        self.email_edit.setMaxLength(50)
        self.email_edit.setObjectName("email_edit")
        self.password_edit = QtWidgets.QLineEdit(self.account_info_page)
        self.password_edit.setGeometry(QtCore.QRect(90, 100, 261, 20))
        self.password_edit.setMaxLength(30)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.password_edit.setObjectName("password_edit")
        self.label_4 = QtWidgets.QLabel(self.account_info_page)
        self.label_4.setGeometry(QtCore.QRect(19, 100, 61, 20))
        self.label_4.setObjectName("label_4")
        self.update_info_button = QtWidgets.QPushButton(self.account_info_page)
        self.update_info_button.setGeometry(QtCore.QRect(90, 130, 113, 32))
        self.update_info_button.setObjectName("update_info_button")
        self.toolBox.addItem(self.account_info_page, "")
        reader_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(reader_window)
        self.toolBox.setCurrentIndex(2)
        self.tab_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(reader_window)

    def retranslateUi(self, reader_window):
        _translate = QtCore.QCoreApplication.translate
        reader_window.setWindowTitle(_translate("reader_window", "your library"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.order_statuses_tab), _translate("reader_window", "order statuses"))
        self.books_table.setSortingEnabled(True)
        item = self.books_table.horizontalHeaderItem(0)
        item.setText(_translate("reader_window", "add to order"))
        item = self.books_table.horizontalHeaderItem(1)
        item.setText(_translate("reader_window", "book name"))
        item = self.books_table.horizontalHeaderItem(2)
        item.setText(_translate("reader_window", "author"))
        item = self.books_table.horizontalHeaderItem(3)
        item.setText(_translate("reader_window", "genres"))
        self.create_order_button.setText(_translate("reader_window", "create order"))
        self.label_5.setText(_translate("reader_window", "return date:"))
        self.label_6.setText(_translate("reader_window", "your order:"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.create_order_tab), _translate("reader_window", "create order"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.library_page), _translate("reader_window", "<books>"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.events_page), _translate("reader_window", "<events>"))
        self.label.setText(_translate("reader_window", "name:"))
        self.label_2.setText(_translate("reader_window", "phone:"))
        self.label_3.setText(_translate("reader_window", "email:"))
        self.label_4.setText(_translate("reader_window", "password:"))
        self.update_info_button.setText(_translate("reader_window", "update info"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.account_info_page), _translate("reader_window", "<account info>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    reader_window = QtWidgets.QMainWindow()
    ui = Ui_reader_window()
    ui.setupUi(reader_window)
    reader_window.show()
    sys.exit(app.exec())
