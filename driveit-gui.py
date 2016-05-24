import glob
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow

from base import SharedBase
from ui import Ui_MainWindow


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.do)
        self.lineEdit.returnPressed.connect(self.do)

    def do(self):
        try:
            self.lineEdit.setDisabled(True)
            self.user_input_url = self.lineEdit.text()
            self.pushButton.setDisabled(True)
            self.checkBox.setDisabled(True)
            self.spinBox.setDisabled(True)
            self.label.setDisabled(True)
            self.base = SharedBase(self.user_input_url)
            self.site_name = self.base.get_site_name()
            if self.checkBox.isChecked():
                checkbox_value = self.spinBox.value()
            else:
                checkbox_value = False
            self.work = WorkingThread(self.site_name, self.user_input_url, checkbox_value)
            self.work.status_report_signal.connect(self.status_receive_signal)
            self.work.progress_report_signal.connect(self.progress_receive_signal)
            self.work.stop_signal.connect(self.stop_signal)
            self.work.start()
        except NameError as e:
            self.stop_signal('Website %s illegal or not supported' % e)

    def status_receive_signal(self, text):
        self.statusBar().showMessage(text)

    def progress_receive_signal(self, progress):
        self.progressBar.setProperty("value", progress)

    def stop_signal(self, text=''):
        self.pushButton.setDisabled(False)
        self.lineEdit.setDisabled(False)
        self.checkBox.setDisabled(False)
        self.spinBox.setDisabled(False)
        self.label.setDisabled(False)
        self.statusBar().showMessage(text)


class WorkingThread(QThread):
    status_report_signal = pyqtSignal(str)
    progress_report_signal = pyqtSignal(float)
    stop_signal = pyqtSignal(str)

    def __init__(self, site_name, url, checkbox_value):
        super(WorkingThread, self).__init__()
        self.site_name = site_name
        self.user_input_url = url
        self.latest_limit = checkbox_value

    def run(self):
        if self.site_name == 'dm5':
            from sites import DM5 as SiteClass
        elif self.site_name == 'ck101':
            from sites import Ck101 as SiteClass
        elif self.site_name == 'dmzj':
            from sites import Dmzj as SiteClass
        elif self.site_name == 'ehentai':
            from sites import Ehentai as SiteClass
        try:
            self.website_object = SiteClass(self.user_input_url)
            self.comic_name = self.website_object.get_name()
            self.ref_box = self.website_object.get_parent_info()
            self.status_report_signal.emit('%s, total %d chapters detected.' % (self.comic_name, len(self.ref_box)))
            if self.latest_limit is not False:
                if self.latest_limit > len(self.ref_box):
                    raise ValueError
                self.ref_box = self.ref_box[-self.latest_limit:]
            self.main_loop(self.ref_box)
        except ValueError as e:
            self.stop_signal.emit('Chapters selected out of range, maximum %s chapters' % len(self.ref_box))
        except ConnectionError as e:
            self.stop_signal.emit('%s, consider using a proxy or a VPN.' % e)

    def main_loop(self, refer_box):
        for ref_tuple in refer_box:
            title, parent_link = ref_tuple
            total_page = self.website_object.get_page_info(parent_link)
            for page in range(1, total_page + 1):
                vague_path = self.website_object.get_path(self.comic_name, title, page) + '*'
                if glob.glob(vague_path):
                    self.status_report_signal.emit('%s page %d already existed.' % (title, page))
                else:
                    try:
                        link = self.website_object.get_image_link(parent_link, page)
                        self.status_report_signal.emit('Downloading %s' % title)
                        self.website_object.down(self.comic_name, parent_link, link, title, page)
                        progress = page / self.website_object.get_page_info(parent_link)
                        self.progress_report_signal.emit(progress * 100)
                    except:
                        errlog = 'Error occurred when downloading %s, Page %d.' % (title, page)
                        self.status_report_signal.emit(errlog)
        self.stop_signal.emit('All Done!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
