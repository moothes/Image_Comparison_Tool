import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from load_win import LoadWindow, SetNumber

from math import *
import numpy as np
import os


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        
        screenRect = QApplication.desktop().screenGeometry()
        self.sh = screenRect.height()
        self.sw = screenRect.width()
        
        
        self.num_fold = 4
        self.folders = None
        self.img_list = None
        self.num_img = 0
        
        self.listview = None
        self.setWindowTitle('Image Viewer')  
        self.lbls = []
        self.f_names = []
        self.initUI()

        
    def initUI(self):
        self.row = floor(sqrt(self.num_fold))
        self.col = ceil(self.num_fold /self.row)
        
        self.img_size = 280
        self.pad = 30
        
 
        #print(self.height)
        #print(self.width)
        
        win_w = 260 + self.col * (self.img_size + self.pad)
        win_h = 80 + self.row * (self.img_size + self.pad)
        self.setGeometry((self.sw - win_w) // 2, (self.sh - win_h) // 2, win_w, win_h)
        #self.setGeometry(20, 50, win_w, win_h)
        self.adjustSize()
        self.setFixedSize(win_w, win_h)
        
        self.statusBar().showMessage('Ready!!!')
        
        # main menu
        setAct = QAction('Setting', self)
        setAct.setStatusTip('Set number of folders')
        #setAct.triggered.connect(self.child_show)
        setAct.triggered.connect(lambda: self.child_show(SetNumber))
        
        
        loadAct = QAction('Load', self)
        loadAct.setStatusTip('Select image folders')
        #loadAct.triggered.connect(self.child_show)
        loadAct.triggered.connect(lambda: self.child_show(LoadWindow))

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        #exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        menubar.clear()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(setAct)
        fileMenu.addAction(loadAct)
        fileMenu.addAction(exitAct)
        
        
        list_lbl = QLabel(self)
        list_lbl.setGeometry(40, 50, 180, 20)
        list_lbl.setText('Image list:')
        
        if self.listview is None:
            #self.listview.deleteLater()
            self.listview = QListWidget(self)
            self.listview.clicked.connect(self.checkItem)
        self.listview.setGeometry(40, 70, 180, self.row * (self.img_size + self.pad) - self.pad)
        #self.layout().addWidget(self.listview)
        
        old_num = len(self.lbls)
        if old_num < self.num_fold:
            for i in range(self.num_fold):
                if i >= old_num:
                    lbl = QLabel(self)
                    f_name = QLabel(self)
                    
                    lbl.setStyleSheet("QLabel{background:white;}"
                                      "QLabel{color:rgb(0,0,0,120);font-size:25px;font-weight:bold;font-family:宋体;}"
                                     )
                    lbl.setAlignment(Qt.AlignCenter)
                    lbl.setText('Folder {}'.format(i))
                    lbl.mouseMoveEvent = self.mouseMove
                    #lbl.installEventFilter(self.mouseMoveEvent(self))
                    #lbl.moved.connect(self.mouseMoveEvent)
                    
                    x = i % self.col
                    y = i // self.col
                    lbl.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 70, self.img_size, self.img_size)
                    
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 50, 60, 20)
                    
                    self.lbls.append(lbl)
                    self.f_names.append(f_name)
                    
                    self.layout().addWidget(lbl)
                    self.layout().addWidget(f_name)
                
                else:
                    lbl = self.lbls[i]
                    f_name = self.f_names[i]
                    
                    x = i % self.col
                    y = i // self.col
                    lbl.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 70, self.img_size, self.img_size)
                    
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 50, 60, 20)
        else:
            for i in range(old_num):
                lbl = self.lbls[i]
                f_name = self.f_names[i]
                if i < self.num_fold:
                    x = i % self.col
                    y = i // self.col
                    lbl.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 70, self.img_size, self.img_size)
                    
                    f_name.setText('Folder {}:'.format(i))
                    f_name.setGeometry(x * (self.img_size + self.pad) + 250, y * (self.img_size + self.pad) + 50, 60, 20)
                else:
                    lbl.deleteLater()
                    f_name.deleteLater()

            self.lbls = self.lbls[:self.num_fold]
            self.f_names = self.f_names[:self.num_fold]
        
        self.show()
        
    def checkItem(self, index):
        self.show_img(self.folders, index.data())

    def child_show(self, window):
        if window.__name__ == 'SetNumber':
            self.s_load = window(self.num_fold)
            self.s_load.set_number.connect(self.set_number)
            self.s_load.show()
        elif window.__name__ == 'LoadWindow':
            self.w_load = window(self.num_fold, self.folders, self.img_list, self.num_img)
            self.w_load.window_close_signal.connect(self.get_folds)
            self.w_load.show()
        
    def set_number(self):
        self.num_fold = self.s_load.num_fold
        #print(self.num_fold)
        self.initUI()
    
    def get_folds(self):
        self.folders = self.w_load.folds
        self.img_list = self.w_load.img_list
        self.num_img = self.w_load.num_img
        
        if self.folders[0] == '' or not self.num_img:
            return
        
        self.listview.clear()
        self.listview.addItems(self.img_list)
        self.listview.setCurrentRow(0)
        
        self.show_img(self.folders, self.img_list[0])
        self.statusBar().showMessage('Load image complete!')

    def show_img(self, folds, name):
        assert len(folds) == self.num_fold
        for i, fold in enumerate(folds):
            if fold == '':
                continue
            self.f_names[i].setText(fold.split('/')[-1] + ':')
            path = os.path.join(fold, name)
            if not os.path.exists(path):
                self.lbls[i].setText('No Image!')
                continue
            
            scaledPixmap = QPixmap(path).scaled(QSize(self.img_size, self.img_size))
            self.lbls[i].setPixmap(scaledPixmap)

    def keyPressEvent(self, event):
        # 1677723 4-7 左上右下
        if event.key() == 16777234:
            # left
            sel_idx = self.listview.currentRow()
            if sel_idx > 0:
                sel_idx -= 1
            self.show_img(self.folders, self.img_list[sel_idx])
            self.listview.setCurrentRow(sel_idx)
            
            msg = 'total image: {}, now: {} .'.format(self.num_img, sel_idx)
            self.statusBar().showMessage(msg)
            
        if event.key() == 16777236:
            # right
            sel_idx = self.listview.currentRow()
            if sel_idx < (self.num_img - 1):
                sel_idx += 1
            self.show_img(self.folders, self.img_list[sel_idx])
            self.listview.setCurrentRow(sel_idx)
            
            msg = 'total image: {}, now: {} .'.format(self.num_img, sel_idx)
            self.statusBar().showMessage(msg)

    def mouseMove(self, e):
        x = e.pos().x()
        y = e.pos().y()

        gx = e.globalPos().x()
        gy = e.globalPos().y()
        ind_x = (gx - 770) // (self.img_size + self.pad) # = x *  + 250+ m 
        ind_y = (gy - 260) // (self.img_size + self.pad) # + 70 + m
        index = np.clip(self.col * ind_y + ind_x, 0, self.num_fold-1)
        
        #pix = self.lbls[index].pixmap()
        #val = pix.toImage().pixel(x, y)
        #colors = QColor(val).getRgbF()
        #print(colors)
        #self.statusBar().showMessage('x: {}, y: {}, Value: {}.'.format(x, y, val))
        #print(gx, gy, index)

        x = 0 if x < 0 else x
        y = 0 if y < 0 else y
        x = self.img_size - 1 if x > self.img_size - 1 else x
        y = self.img_size - 1 if y > self.img_size - 1 else y


        for i in range(self.num_fold):
            pix = self.lbls[i].pixmap()
            if pix is None:
                continue
            im = pix.toImage()
            value = qRgb(255, 255, 0)
            
            im.setPixel(x-1, y-1, value)
            im.setPixel(x-1, y  , value)
            im.setPixel(x-1, y+1, value)
            im.setPixel(x  , y-1, value)
            im.setPixel(x  , y  , value)
            im.setPixel(x  , y+1, value)
            im.setPixel(x+1, y-1, value)
            im.setPixel(x+1, y  , value)
            im.setPixel(x+1, y+1, value)
            
            
            self.lbls[i].setPixmap(QPixmap.fromImage(im))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('WindowsXP')
    ex = Example()
    sys.exit(app.exec_())