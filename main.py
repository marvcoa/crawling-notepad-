import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import webbrowser
from PyQt5 import QtCore
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time

form_class = uic.loadUiType("C:\\Users\\82109\\Desktop\\note.ui")[0]
form_class2 = uic.loadUiType("C:\\Users\\82109\\Desktop\\find.ui")[0]
form_class3 = uic.loadUiType("C:\\Users\\82109\\Desktop\\change.ui")[0]


class newmake(QDialog):
    def __init__(self, parent):
        super(newmake, self).__init__(parent)
        uic.loadUi("C:\\Users\\82109\\Desktop\\new2.ui", self)
        self.pushButton_save.clicked.connect(self.save_ex)
        self.pushButton_saveno.clicked.connect(self.saveno)
        self.pushButton_cancle.clicked.connect(self.saveno)
        self.show()

    def save_ex(self):
        mainWindow.saveFunction()
        self.accept()

    def saveno(self):
        mainWindow.cleartext()
        self.accept()

    def close(self):
        self.accept()


class findw(QDialog):
    a = 'a'

    def __init__(self, parent):
        super(findw, self).__init__(parent)
        uic.loadUi("C:\\Users\\82109\\Desktop\\find.ui", self)
        self.show()

        self.parent = mainWindow
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit
        self.pos = 0

        self.str = "offsets: 1.23 .50 71.00 6.00"
        self.pushButton_findnext.clicked.connect(self.find_next)
        self.pushButton_cancle.clicked.connect(self.close)
        self.radioButton_up.clicked.connect(self.updown)
        self.radioButton_down.clicked.connect(self.updown)
        self.updownd = "down"
        self.text = self.pe.toPlainText()
        self.pat = self.lineEdit.text()
        self.reg = QtCore.QRegExp(self.pat)

        pos = self.cursor.position()
        self.index = self.reg.lastIndexIn(self.text, pos)

    def updown(self):
        if self.radioButton_up.isChecked():
            self.updownd = "up"
            print('up')
        elif self.radioButton_down.isChecked():
            self.updownd = "down"
            print('down')

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def setCursor(self, start, end):
        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)
        self.pe.setTextCursor(self.cursor)

    # 찾기 기능 현재 맨 앞에 있는것만 검색됨)
    def find_next(self):
        #찾기 창에서 값 입력한 값 불러오는거
        self.pat = self.lineEdit.text()
        global  pat
        pat = self.lineEdit.text()
        self.reg = QtCore.QRegExp(self.pat)
        self.cursor = self.parent.plainTextEdit.textCursor()
        pos = self.cursor.position()

        self.index = self.reg.indexIn(self.text, pos)

        if self.checkBox.isChecked():
            cs = QtCore.Qt.CaseSensitive
        else:
            cs = QtCore.Qt.CaseInsensitive

        self.reg.setCaseSensitivity(cs)

        #내림차순
        if self.index != -1:
            self.setCursor(self.index, len(self.pat)+self.index)


        #오름차순
        if self.updownd == "down":
            self.index = self.reg.indexIn(self.text, pos)
        else:
            pos -= len(self.pat) + 1
            self.index = self.reg.lastIndexIn(self.text, pos)

        if self.index != -1:
            self.setCursor(self.index, len(self.pat)+self.index)

    def find_next2(self):
        reg = QtCore.QRegExp(pat)
        self.plainTextEdit.find(reg)


class changeWindow(QDialog):
    def __init__(self, parent):
        super(changeWindow, self).__init__(parent)
        uic.loadUi("C:\\Users\\82109\\Desktop\\change.ui", self)
        self.show()

        self.parent = mainWindow
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit
        self.text = self.pe.toPlainText()
        self.updownd = "down"

        self.pushButton_findnext.clicked.connect(self.find_next)
        self.pushButton_cancel.clicked.connect(self.close)
        self.pushButton_change.clicked.connect(self.changeFunction)
        self.pushButton_changeall.clicked.connect(self.changeallFunction)

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
            self.pushButton_change.setEnabled(True)
            self.pushButton_changeall.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)
            self.pushButton_change.setEnabled(False)
            self.pushButton_changeall.setEnabled(False)

    def setCursor(self, start, end):
        self.cursor.setPosition(start)
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)
        self.pe.setTextCursor(self.cursor)

    def find_next(self):
        #찾기 창에서 값 입력한 값 불러오는거
        self.pat = self.lineEdit.text()
        global  pat
        pat = self.lineEdit.text()
        self.reg = QtCore.QRegExp(self.pat)
        self.cursor = self.parent.plainTextEdit.textCursor()
        pos = self.cursor.position()

        self.index = self.reg.indexIn(self.text, pos)

        if self.checkBox.isChecked():
            cs = QtCore.Qt.CaseSensitive
        else:
            cs = QtCore.Qt.CaseInsensitive

        self.reg.setCaseSensitivity(cs)

        #내림차순
        if self.index != -1:
            self.setCursor(self.index, len(self.pat)+self.index)


        #오름차순
        if self.updownd == "down":
            self.index = self.reg.indexIn(self.text, pos)
        else:
            pos -= len(self.pat) + 1
            self.index = self.reg.lastIndexIn(self.text, pos)

        if self.index != -1:
            self.setCursor(self.index, len(self.pat)+self.index)

    def changeFunction(self):
        self.cursor = self.parent.plainTextEdit.textCursor()
        find = self.lineEdit.text()
        cursor2 = self.pe.toPlainText()[self.cursor.selectionStart():self.cursor.selectionEnd()]

        if not self.checkBox.isChecked():
            find = find.lower()
            cursor2 = cursor2.lower()
        if find != cursor2:
            self.find_next()
        else:
            self.cursor.insertText(self.lineEdit_changeline.text())
            self.find_next()

    def changeallFunction(self):
        search = self.lineEdit.text()
        length = len(search)

        if not self.checkBox.isChecked():
            search = search.lower()
        while True:
            if not self.checkBox.isChecked():
                index = self.parent.plainTextEdit.toPlainText().lower().find(search)
            else:
                index = self.parent.plainTextEdit.toPlainText().find(search)
            if index == -1:
                break
            self.parent.plainTextEdit.setPlainText(self.parent.plainTextEdit.toPlainText()[:index] + self.lineEdit_changeline.text() + self.parent.plainTextEdit.toPlainText()[index + length:])

class infowindow(QDialog):
    def __init__(self, parent):
        super(infowindow, self).__init__(parent)
        uic.loadUi("C:\\Users\\82109\\Desktop\\info.ui", self)
        self.show()


class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cursor = self.plainTextEdit.textCursor()
        self.pe = self.plainTextEdit
        self.text = self.pe.toPlainText()
        self.reg = QtCore.QRegExp()
        self.updownd = "o"
        self.colorLabel = QLabel()
        self.zoom = 0
        self.status_bar = True
        self.ln = 0
        self.col = 0

        self.action_newmake.triggered.connect(self.newmakeFunction)
        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_newfile.triggered.connect(self.newfileFunction)
        self.action_saveas.triggered.connect(self.saveasFuntion)
        self.action_pagesetting.triggered.connect(self.pagesettingFuntion)
        self.action_printfile.triggered.connect(self.printfileFuntion)
        self.action_closewin.triggered.connect(self.closewinFuntion)
        self.action_undo.triggered.connect(self.undoFuntion)
        self.action_copy.triggered.connect(self.copyFuntion)
        self.action_cut.triggered.connect(self.cutFuntion)
        self.action_paste.triggered.connect(self.pasteFuntion)
        self.action_delete.triggered.connect(self.deleteFuntion)
        self.action_search.triggered.connect(self.searchFuntion)
        self.action_find.triggered.connect(self.findFuntion)
        self.action_nextfind.triggered.connect(self.find_nextFuntion)
        self.action_nextfind2.triggered.connect(self.find_next2Funtion)
        self.action_selectall.triggered.connect(self.selectallFuntion)
        self.action_time.triggered.connect(self.timeFuntion)
        self.action_change.triggered.connect(self.changeFuntion)
        self.action_font.triggered.connect(self.fontFuntion)
        self.action_zoom_in.triggered.connect(self.zoom_inFuntion)
        self.action_zoom_out.triggered.connect(self.zoom_outFuntion)
        self.action_zoom_clean.triggered.connect(self.zoomcleanFunction)
        self.action_status.triggered.connect(self.statusFunction)
        self.action_info.triggered.connect(self.infoFunction)
        self.action_help.triggered.connect(self.helpFuntion)
        self.action_feedback.triggered.connect(self.feedbackFuntion)
        self.action_crawling.triggered.connect(self.crawlingFuntion)

    def fontFuntion(self):
        font, fc = QFontDialog.getFont()
        if fc:
            self.colorLabel.setFont(font)
            app.setFont(font)

    def openFunction(self):
        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            with open(fname[0], encoding='UTF8') as f:
                data = f.read()
            self.plainTextEdit.setPlainText(data)
        print("open {}".format(fname[0]))

    def saveFunction(self):
         fname = QFileDialog.getOpenFileName(self)
         if fname[0]:
            data = self.plainTextEdit.toPlainText()

            with open(fname[0], 'w', encoding='UTF8') as f:
              f.write(data)

            print("save{}".format(fname[0]))

    def saveasFuntion(self):
        fname = QFileDialog.getSaveFileName(self,'save as','.txt',)

        if fname[0]:
            data = self.plainTextEdit.toPlainText()

            with open(fname[0], 'w', encoding='UTF8') as f:
                f.write(data)

    def pagesettingFuntion(self):

        page = QPageSetupDialog(self)
        if page.exec() == QDialog.Accepted:
         QPageSetupDialog

    def printfileFuntion(self):

        printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QDialog.Accepted:
            qp = QPainter()
            qp.begin(printer)

            self.render(qp)

            qp.end()

    def newfileFunction(self):

        self.newWindow = NewWindow(self)
        self.newWindow.show()

    def newmakeFunction(self):
        newmake(self)

    def cleartext(self):
        self.plainTextEdit.clear()

    def closewinFuntion(self):
           self.destroy()

    def undoFuntion(self):
        self.plainTextEdit.undo()

    def copyFuntion(self):
        self.plainTextEdit.copy()

    def cutFuntion(self):
        self.plainTextEdit.cut()

    def pasteFuntion(self):
        self.plainTextEdit.paste()

    def deleteFuntion(self):
        self.plainTextEdit.setPlainText('')

    def searchFuntion(self):
        url ="http://www.naver.com"
        webbrowser.open(url)

    def findFuntion(self):
        findw(self)

    def selectallFuntion(self):
        self.plainTextEdit.selectAll()

    def timeFuntion(self):
        timea = time.strftime('%p %X %y-%m-%d', time.localtime((time.time())))
        self.plainTextEdit.appendPlainText(timea)
        print(timea)

    def find_nextFuntion(self):
        findw.find_next2(self)

    def find_next2Funtion(self):
        findw.find_next3(self)

    def changeFuntion(self):
        changeWindow(self)

    def statusFunction(self):
        if self.status_bar:
            self.status_bar = False
            self.statusBar().hide()
        else:
            self.status_bar = True
            self.statusBar().show()

    def zoom_inFuntion(self):
        if self.zoom < 100:
            self.plainTextEdit.zoomIn()
            self.zoom += 1

    def zoom_outFuntion(self):
        if self.zoom > -100:
            self.plainTextEdit.zoomOut()
            self.zoom -= 1

    def zoomcleanFunction(self):
        if self.zoom > 0:
            self.plainTextEdit.zoomOut(self.zoom)
        elif self.zoom < 0:
            self.plainTextEdit.zoomIn(abs(self.zoom))
        self.zoom = 0

    def infoFunction(self):
        infowindow(self)

    def helpFuntion(self):
        url_help = 'https://support.microsoft.com/ko-kr/windows/%EB%A9%94%EB%AA%A8%EC%9E%A5%EC%9D%98-%EB%8F%84%EC%9B%80%EB%A7%90-4d68c388-2ff2-0e7f-b706-35fb2ab88a8c'
        webbrowser.open(url_help)

    def feedbackFuntion(self):
        url_feedback = 'https://github.com/marvcoa'
        webbrowser.open(url_feedback)

    def crawlingFuntion(self):
        htmlc = self.plainTextEdit.toPlainText()
        print(htmlc)
        html = urlopen('https://search.naver.com/search.naver?where=news&sm=tab_jum&query='+urllib.parse.quote_plus(htmlc))
        bs = BeautifulSoup(html, "html.parser")
        title = bs.find_all(class_ = 'news_tit')

        for link in title:
            ti_a = link.attrs['title']
            ti_b = link.attrs['href']
            self.plainTextEdit.appendPlainText(ti_a)
            self.plainTextEdit.appendPlainText(ti_b)
            self.plainTextEdit.appendPlainText("")


class NewWindow(QMainWindow, form_class):

    def __init__(self, parent=WindowClass):
        super(NewWindow, self).__init__(parent)
        self.setupUi(self)


app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()