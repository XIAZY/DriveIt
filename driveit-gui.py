from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from window import Ui_MainWindow
from base import SharedBase
import sys


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
            self.base = SharedBase(self.user_input_url)
            self.site_name = self.base.get_site_name()
            self.work = WorkingThread(self.site_name, self.user_input_url)
            self.work.status_report_signal.connect(self.status_receive_signal)
            self.work.progress_report_signal.connect(self.progress_receive_signal)
            self.work.start()
        except NameError as e:
            self.statusBar().showMessage('Website %s illegal or not supported' % e)
            self.pushButton.setDisabled(False)

    def status_receive_signal(self, text):
        self.statusBar().showMessage(text)
        if text == 'All Done!':
            self.pushButton.setDisabled(False)
            self.lineEdit.setDisabled(False)

    def progress_receive_signal(self, progress):
        self.progressBar.setProperty("value", progress)


class WorkingThread(QThread):
    status_report_signal = pyqtSignal(str)
    progress_report_signal = pyqtSignal(float)

    def __init__(self, site_name, url):
        super(WorkingThread, self).__init__()
        self.site_name = site_name
        self.user_input_url = url

    def run(self):
        if self.site_name == 'dm5':
            from sites import DM5 as SiteClass
        elif self.site_name == 'ck101':
            from sites import Ck101 as SiteClass
        self.website_object = SiteClass(self.user_input_url)
        self.comic_name = self.website_object.get_name()
        self.ref_box = self.website_object.get_chapter_info()
        self.status_report_signal.emit('%s, total %d chapters detected.' % (self.comic_name, max(self.ref_box.keys())))
        self.main_loop(self.ref_box)
        if self.website_object.is_volume() is True:
            self.main_loop(self.website_object.get_volume_info(), True)

    def main_loop(self, refer_box, is_volume=False):
        total_parents = max(refer_box.keys())
        if is_volume is True:
            parent_str = 'Volume'
        else:
            parent_str = 'Chapter'
        for parent in range(1, total_parents + 1):
            if parent in refer_box.keys():
                cid = refer_box[parent]
                for page in range(1, self.website_object.get_page_info(cid) + 1):
                    link = self.website_object.get_image_link(cid, page)
                    try:
                        self.status_report_signal.emit(
                                'Downloading %s %s %s' % (self.comic_name, parent_str, parent))
                        progress = page / self.website_object.get_page_info(cid)
                        self.website_object.down(self.comic_name, cid, link, parent, page, is_volume)
                        self.progress_report_signal.emit(progress * 100)
                    except:
                        self.status_report_signal.emit(
                                'Error occurred when downloading %s %d, Page %d.' % (parent_str, parent, page))
            else:
                self.status_report_signal.emit('Chapter %d cannot be found.' % parent)
        self.status_report_signal.emit('All Done!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
