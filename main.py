from PyQt6 import QtWidgets
from ui.login.login import complete_login_window

import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    login_ui = complete_login_window()
    login_ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())
