# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI3.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(375, 470)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 20)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ThumbnailView = QtWidgets.QLabel(self.centralwidget)
        self.ThumbnailView.setMaximumSize(QtCore.QSize(350, 300))
        self.ThumbnailView.setAlignment(QtCore.Qt.AlignCenter)
        self.ThumbnailView.setObjectName("ThumbnailView")
        self.verticalLayout_5.addWidget(self.ThumbnailView)
        self.StackedMulti1 = QtWidgets.QWidget(self.centralwidget)
        self.StackedMulti1.setMaximumSize(QtCore.QSize(16777215, 30))
        self.StackedMulti1.setObjectName("StackedMulti1")
        self.verticalLayout_5.addWidget(self.StackedMulti1)
        self.Options = QtWidgets.QWidget(self.centralwidget)
        self.Options.setMaximumSize(QtCore.QSize(16777215, 50))
        self.Options.setObjectName("Options")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.Options)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.HighestQual = QtWidgets.QCheckBox(self.Options)
        self.HighestQual.setObjectName("HighestQual")
        self.horizontalLayout_4.addWidget(self.HighestQual)
        self.AudioOnly = QtWidgets.QCheckBox(self.Options)
        self.AudioOnly.setObjectName("AudioOnly")
        self.horizontalLayout_4.addWidget(self.AudioOnly)
        self.verticalLayout_5.addWidget(self.Options)
        self.StackedMulti2 = QtWidgets.QWidget(self.centralwidget)
        self.StackedMulti2.setMaximumSize(QtCore.QSize(16777215, 100))
        self.StackedMulti2.setObjectName("StackedMulti2")
        self.verticalLayout_5.addWidget(self.StackedMulti2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 375, 22))
        self.menubar.setObjectName("menubar")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.actionShortcuts = QtWidgets.QAction(MainWindow)
        self.actionShortcuts.setObjectName("actionShortcuts")
        self.actionYoutube_Sign_In = QtWidgets.QAction(MainWindow)
        self.actionYoutube_Sign_In.setObjectName("actionYoutube_Sign_In")
        self.menuSettings.addAction(self.actionShortcuts)
        self.menuSettings.addAction(self.actionYoutube_Sign_In)
        self.menubar.addAction(self.menuSettings.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.ThumbnailView.setText(_translate("MainWindow", "Welcome to Qtube, please enter a valid YouTube URL"))
        self.HighestQual.setText(_translate("MainWindow", "Highest Quality"))
        self.AudioOnly.setText(_translate("MainWindow", "Audio Only"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionShortcuts.setText(_translate("MainWindow", "Shortcuts"))
        self.actionYoutube_Sign_In.setText(_translate("MainWindow", "Youtube Sign In"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
