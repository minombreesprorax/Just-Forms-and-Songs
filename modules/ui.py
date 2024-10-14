# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'launcherpMhNpY.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTreeView, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(497, 324)
        MainWindow.setWindowIcon(QIcon("./icon1.png"))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Arial Rounded MT"])
        font.setPointSize(24)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.LevelList = QTreeView(self.centralwidget)
        self.LevelList.setObjectName(u"LevelList")
        self.LevelList.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        self.verticalLayout.addWidget(self.LevelList)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setPlaceholderText(u"level ID")

        self.verticalLayout.addWidget(self.lineEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Close = QPushButton(self.centralwidget)
        self.Close.setObjectName(u"Close")

        self.horizontalLayout.addWidget(self.Close)

        self.Launch = QPushButton(self.centralwidget)
        self.Launch.setObjectName(u"Launch")

        self.horizontalLayout.addWidget(self.Launch)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.Close.released.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"JFAS loader", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; font-weight:900;\">Just Forms and Songs</span></p><p align=\"center\"><span style=\" font-size:8pt;\">AKA: JSAB but made in python. (V 1.2)</span></p></body></html>", None))
        self.Close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.Launch.setText(QCoreApplication.translate("MainWindow", u"Launch", None))
    # retranslateUi

