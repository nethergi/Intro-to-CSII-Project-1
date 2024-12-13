from PyQt6.QtWidgets import *
import gui



def main():
    app = QApplication([])
    windowRoot = QMainWindow()

    window = gui.Ui_MainWindow()
    window.setupUi(windowRoot)

    windowRoot.show()
    app.exec()

    

if __name__ == "__main__":
    main()