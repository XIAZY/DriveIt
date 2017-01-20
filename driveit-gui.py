import glob
import os
import sys
from multiprocessing.pool import ThreadPool

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi

from base import SharedBase


class MyMainWindow(QMainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.do)
        self.lineEdit.returnPressed.connect(self.do)
        self.pushButton_browse_file.clicked.connect(self.show_file_dialog)
        self.lineEdit_save_location.setText(os.getcwd())
        self.lineEdit.setFocus()

    def show_file_dialog(self):
        selected_dir = QFileDialog.getExistingDirectory(self, caption='Choose Directory', directory=os.getcwd())
        self.lineEdit_save_location.setText(selected_dir)

    def do(self):
        try:
            self.lineEdit.setDisabled(True)
            self.user_input_url = self.lineEdit.text()
            self.pushButton.setDisabled(True)
            self.checkBox.setDisabled(True)
            self.spinBox_fetch_limit.setDisabled(True)
            self.spinBox_threads.setDisabled(True)
            self.label_chapters.setDisabled(True)
            self.label_threads.setDisabled(True)
            self.label_save.setDisabled(True)
            self.lineEdit_save_location.setDisabled(True)
            self.save_dir = self.lineEdit_save_location.text()
            self.pushButton_browse_file.setDisabled(True)
            self.base = SharedBase(self.user_input_url)
            self.site_name = self.base.get_site_name()
            if self.checkBox.isChecked():
                checkbox_value = self.spinBox_fetch_limit.value()
            else:
                checkbox_value = False
            threads = self.spinBox_threads.value()
            self.work = WorkingThread(self.site_name, self.user_input_url, checkbox_value, threads, self.save_dir)
            self.work.status_report_signal.connect(self.status_receive_signal)
            self.work.progress_report_signal.connect(self.progress_receive_signal)
            self.work.stop_signal.connect(self.stop_signal)
            self.work.chapter_start_signal.connect(self.chapter_start_receive_signal)
            self.work.start()
        except NameError as e:
            self.stop_signal('Website %s illegal or not supported' % e)

    def status_receive_signal(self, text):
        self.statusBar().showMessage(text)

    def progress_receive_signal(self, is_done):
        self.pages_done += 1
        self.progressBar.setProperty('value', self.pages_done / self.total_pages * 100)

    def chapter_start_receive_signal(self, start_tuple):
        parent_title, total_pages = start_tuple
        self.status_receive_signal('Downloading %s' % parent_title)
        self.pages_done = 0
        self.total_pages = total_pages

    def stop_signal(self, text=''):
        self.lineEdit.setDisabled(False)
        self.pushButton.setDisabled(False)
        self.checkBox.setDisabled(False)
        self.spinBox_fetch_limit.setDisabled(False)
        self.spinBox_threads.setDisabled(False)
        self.label_chapters.setDisabled(False)
        self.label_threads.setDisabled(False)
        self.label_save.setDisabled(False)
        self.lineEdit_save_location.setDisabled(False)
        self.pushButton_browse_file.setDisabled(False)
        self.statusBar().showMessage(text)
        self.lineEdit.setFocus()


class WorkingThread(QThread):
    status_report_signal = pyqtSignal(str)
    progress_report_signal = pyqtSignal(bool)
    stop_signal = pyqtSignal(str)
    chapter_start_signal = pyqtSignal(tuple)

    def __init__(self, site_name, url, checkbox_value, threads, save_dir):
        super(WorkingThread, self).__init__()
        self.site_name = site_name
        self.user_input_url = url
        self.latest_limit = checkbox_value
        self.threads = threads
        self.save_dir = save_dir

    def run(self):
        if self.site_name == 'dm5':
            from sites import DM5 as SiteClass
        elif self.site_name == 'ck101':
            from sites import Ck101 as SiteClass
        elif self.site_name == 'dmzj':
            from sites import Dmzj as SiteClass
        elif self.site_name == 'manhua_dmzj':
            from sites import manhua_Dmzj as SiteClass
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
        except ValueError:
            self.stop_signal.emit('Chapters selected out of range, maximum %s chapters' % len(self.ref_box))
        except ConnectionError as e:
            self.stop_signal.emit('%s, consider using a proxy or a VPN.' % e)

    def main_loop(self, refer_box):
        # for ref_tuple in refer_box:
        #     title, parent_link = ref_tuple
        #     total_page = self.website_object.get_page_info(parent_link)
        #     for page in range(1, total_page + 1):
        #         vague_path = self.website_object.get_path(self.comic_name, title, page) + '*'
        #         if glob.glob(vague_path):
        #             self.status_report_signal.emit('%s page %d already existed.' % (title, page))
        #         else:
        #             try:
        #                 link = self.website_object.get_image_link(parent_link, page)
        #                 self.status_report_signal.emit('Downloading %s' % title)
        #                 self.website_object.down(self.comic_name, parent_link, link, title, page)
        #                 progress = page / self.website_object.get_page_info(parent_link)
        #                 self.progress_report_signal.emit(progress * 100)
        #             except:
        #                 errlog = 'Error occurred when downloading %s, Page %d.' % (title, page)
        #                 self.status_report_signal.emit(errlog)
        # self.stop_signal.emit('All Done!')
        for refer_tuple in refer_box:
            parent_title, parent_link = refer_tuple
            total_page = self.website_object.get_page_info(parent_link)
            jobs = list()
            for page in range(1, total_page + 1):
                jobs.append((parent_title, parent_link, page, total_page))
            pool_size = self.threads
            pool = ThreadPool(processes=pool_size)
            # self.status_report_signal.emit('Downloading %s' % parent_title)
            self.chapter_start_signal.emit((parent_title, total_page))
            pool.map(self.loop_thread, jobs)
            pool.close()
            pool.join()
        self.stop_signal.emit('All Done!')

    def loop_thread(self, args):
        parent_title, parent_link, page, total_page = args
        vague_path = self.website_object.get_path(self.comic_name, parent_title, page) + '*'
        if glob.glob(vague_path):
            self.status_report_signal.emit('%s page %d already existed.' % (parent_title, page))
        else:
            try:
                link = self.website_object.get_image_link(parent_link, page)
                self.website_object.down(self.comic_name, parent_link, link, parent_title, page, self.save_dir)
                self.progress_report_signal.emit(True)
            except:
                self.status_report_signal.emit('Error occurred when downloading %s, Page %d.' % (parent_title, page))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())
