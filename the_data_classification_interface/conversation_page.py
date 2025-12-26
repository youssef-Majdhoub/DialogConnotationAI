# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'conversation_page.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QSlider,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_page(object):
    def setupUi(self, page):
        if not page.objectName():
            page.setObjectName(u"page")
        page.resize(662, 581)
        self.verticalLayout = QVBoxLayout(page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.conversation_space = QWidget(page)
        self.conversation_space.setObjectName(u"conversation_space")
        self.conversation_space.setStyleSheet(u"background-color: rgba(240, 240, 240,0);")
        self.verticalLayout_4 = QVBoxLayout(self.conversation_space)
        self.verticalLayout_4.setSpacing(25)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 30, -1, -1)
        self.message_1 = QWidget(self.conversation_space)
        self.message_1.setObjectName(u"message_1")
        self.verticalLayout_3 = QVBoxLayout(self.message_1)
        self.verticalLayout_3.setSpacing(30)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.text_1 = QLabel(self.message_1)
        self.text_1.setObjectName(u"text_1")
        font = QFont()
        font.setPointSize(20)
        self.text_1.setFont(font)

        self.verticalLayout_3.addWidget(self.text_1)

        self.connotation_1 = QSlider(self.message_1)
        self.connotation_1.setObjectName(u"connotation_1")
        self.connotation_1.setMinimum(-10)
        self.connotation_1.setMaximum(10)
        self.connotation_1.setTracking(True)
        self.connotation_1.setOrientation(Qt.Orientation.Horizontal)
        self.connotation_1.setInvertedAppearance(False)
        self.connotation_1.setInvertedControls(False)
        self.connotation_1.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.connotation_1.setTickInterval(0)

        self.verticalLayout_3.addWidget(self.connotation_1)


        self.verticalLayout_4.addWidget(self.message_1)

        self.message_2 = QWidget(self.conversation_space)
        self.message_2.setObjectName(u"message_2")
        self.verticalLayout_5 = QVBoxLayout(self.message_2)
        self.verticalLayout_5.setSpacing(30)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.text_2 = QLabel(self.message_2)
        self.text_2.setObjectName(u"text_2")
        self.text_2.setFont(font)

        self.verticalLayout_5.addWidget(self.text_2)

        self.connotation_2 = QSlider(self.message_2)
        self.connotation_2.setObjectName(u"connotation_2")
        self.connotation_2.setMinimum(-10)
        self.connotation_2.setMaximum(10)
        self.connotation_2.setOrientation(Qt.Orientation.Horizontal)
        self.connotation_2.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.verticalLayout_5.addWidget(self.connotation_2)


        self.verticalLayout_4.addWidget(self.message_2)

        self.message_3 = QWidget(self.conversation_space)
        self.message_3.setObjectName(u"message_3")
        self.verticalLayout_6 = QVBoxLayout(self.message_3)
        self.verticalLayout_6.setSpacing(30)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.text_3 = QLabel(self.message_3)
        self.text_3.setObjectName(u"text_3")
        self.text_3.setFont(font)

        self.verticalLayout_6.addWidget(self.text_3)

        self.connotation_3 = QSlider(self.message_3)
        self.connotation_3.setObjectName(u"connotation_3")
        self.connotation_3.setMinimum(-10)
        self.connotation_3.setMaximum(10)
        self.connotation_3.setOrientation(Qt.Orientation.Horizontal)
        self.connotation_3.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.verticalLayout_6.addWidget(self.connotation_3)


        self.verticalLayout_4.addWidget(self.message_3)

        self.message_4 = QWidget(self.conversation_space)
        self.message_4.setObjectName(u"message_4")
        self.verticalLayout_7 = QVBoxLayout(self.message_4)
        self.verticalLayout_7.setSpacing(30)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.text_4 = QLabel(self.message_4)
        self.text_4.setObjectName(u"text_4")
        self.text_4.setFont(font)

        self.verticalLayout_7.addWidget(self.text_4)

        self.connotation_4 = QSlider(self.message_4)
        self.connotation_4.setObjectName(u"connotation_4")
        self.connotation_4.setMinimum(-10)
        self.connotation_4.setMaximum(10)
        self.connotation_4.setOrientation(Qt.Orientation.Horizontal)
        self.connotation_4.setTickPosition(QSlider.TickPosition.TicksBelow)

        self.verticalLayout_7.addWidget(self.connotation_4)


        self.verticalLayout_4.addWidget(self.message_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.verticalLayout.addWidget(self.conversation_space)


        self.retranslateUi(page)

        QMetaObject.connectSlotsByName(page)
    # setupUi

    def retranslateUi(self, page):
        page.setWindowTitle(QCoreApplication.translate("page", u"Form", None))
        self.text_1.setText(QCoreApplication.translate("page", u"TextLabel", None))
        self.text_2.setText(QCoreApplication.translate("page", u"TextLabel", None))
        self.text_3.setText(QCoreApplication.translate("page", u"TextLabel", None))
        self.text_4.setText(QCoreApplication.translate("page", u"text", None))
    # retranslateUi

