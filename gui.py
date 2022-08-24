"""
The web-application changes a .wav file
via Fourier Transform

The application takes a *.wav file as an argument (File->Open).
First and second plots show the signal in signal-time and frequency-time domains respectively.
After a user chooses a frequency band to be deleted,
third and forth plots show the processed signal in two domains just as above.
After that the new file can be saved in *.wav format (File->Save).
"""
import sys
import numpy as np
import soundfile as sf
from PyQt6 import QtGui, QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from librosa import load, display, stft, istft, amplitude_to_db, util
# ---------- mine -----------
from check import check_value, error_window

font = QtGui.QFont()
font.setFamily("Arial")
font.setPointSize(12)


# todo: UiMainWindow
class UiMainWindow(object):

    def __init__(self):
        """
        The class creates the main window of the application
        and defines position and size of its widgets.
        """
        self.central_widget = QtWidgets.QWidget()
        self.graphics_view = QtWidgets.QGraphicsView(self.central_widget)
        self.graphics_view_2 = QtWidgets.QGraphicsView(self.central_widget)
        self.graphics_view_3 = QtWidgets.QGraphicsView(self.central_widget)
        self.graphics_view_4 = QtWidgets.QGraphicsView(self.central_widget)
        self.push_button = QtWidgets.QPushButton(self.central_widget)
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label_2 = QtWidgets.QLabel(self.central_widget)
        self.line_edit = QtWidgets.QLineEdit(self.central_widget)
        self.line_edit_2 = QtWidgets.QLineEdit(self.central_widget)
        self.menubar = QtWidgets.QMenuBar()
        self.menu_file = QtWidgets.QMenu(self.menubar)
        self.action_open = QtGui.QAction()
        self.action_save = QtGui.QAction()
        self.action_exit = QtGui.QAction()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setFixedSize(1030, 900)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
        MainWindow.setWindowTitle('Eufoury')
        MainWindow.setFont(font)
        MainWindow.setCentralWidget(self.central_widget)
        MainWindow.setMenuBar(self.menubar)
        MainWindow.retranslate_ui()
        self.graphics_view.setGeometry(QtCore.QRect(10, 30, 500, 380))
        self.graphics_view_2.setGeometry(QtCore.QRect(520, 30, 500, 380))
        self.graphics_view_3.setGeometry(QtCore.QRect(10, 450, 500, 380))
        self.graphics_view_4.setGeometry(QtCore.QRect(520, 450, 500, 380))
        self.push_button.setGeometry(QtCore.QRect(820, 415, 200, 30))
        self.label.setGeometry(QtCore.QRect(10, 415, 361, 30))
        self.line_edit.setGeometry(QtCore.QRect(310, 415, 60, 30))
        self.label_2.setGeometry(QtCore.QRect(380, 415, 21, 30))
        self.line_edit_2.setGeometry(QtCore.QRect(405, 415, 60, 30))
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menu_file.setEnabled(True)
        self.menu_file.setGeometry(QtCore.QRect(269, 125, 135, 125))
        self.menu_file.setAutoFillBackground(False)
        self.menu_file.setFont(font)
        self.menu_file.addAction(self.action_open)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menubar.addAction(self.menu_file.menuAction())
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.action_exit.triggered.connect(self.close_file)

    @staticmethod
    def close_file():
        sys.exit()

    def retranslate_ui(self):
        self.push_button.setText("Get processed signal")
        self.label.setText("Choose frequency you want to delete from")
        self.label_2.setText("to")
        self.menu_file.setTitle("File")
        self.action_open.setText("Open")
        self.action_save.setText("Save")
        self.action_exit.setText("Exit")


# todo: Plot
class Plot(QtWidgets.QMainWindow, UiMainWindow):

    def __init__(self):
        """
        The class inherits from UiMainWindow class,
        it creates 4 graphic plots for the chosen audio file in 4 graphic views defined in the parental class.
        Moreover, it connects to widgets from UiMainWindow for opening/saving a file or launching processing.
        """
        super(Plot, self).__init__()
        self.setupUi(self)
        self.action_open.triggered.connect(self.original_signal)
        self.action_save.triggered.connect(self.save_signal)
        self.push_button.clicked.connect(self.processed_signal)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene_2 = QtWidgets.QGraphicsScene()
        self.scene_3 = QtWidgets.QGraphicsScene()
        self.scene_4 = QtWidgets.QGraphicsScene()
        self.graphics_view.setScene(self.scene)  # redefine each instance
        self.graphics_view_2.setScene(self.scene_2)
        self.graphics_view_3.setScene(self.scene_3)
        self.graphics_view_4.setScene(self.scene_4)
        self.figure = Figure(figsize=(4.9, 3.4), facecolor='w', layout='tight')
        self.figure_2 = Figure(figsize=(4.9, 3.4), facecolor='w', layout='tight')
        self.figure_3 = Figure(figsize=(4.9, 3.4), facecolor='w', layout='tight')
        self.figure_4 = Figure(figsize=(4.9, 3.4), facecolor='w', layout='tight')
        self.axes = self.figure.gca()
        self.axes_2 = self.figure_2.gca()
        self.axes_3 = self.figure_3.gca()
        self.axes_4 = self.figure_4.gca()

    # todo: original signal
    def original_signal(self):
        """
        The function opens a file to process
        and creates upper left (signal-time) and upper-right (frequency-time) plots,
        the second plot is calculated using Short Time Fourier Transform.
        :return: None
        """
        self.name, _ = QtWidgets.QFileDialog.getOpenFileName(filter='*.wav')

        # region 1st window
        original_y, sr = load(self.name)
        self.axes.clear()
        display.waveshow(original_y, ax=self.axes)
        self.axes.grid(which='major')
        self.axes.minorticks_on()
        self.axes.grid(which='minor')
        self.axes.set_xlabel('Duration, s')
        self.axes.set_ylabel('Signal')
        self.axes.set_title('Original signal in time domain')
        self.canvas = FigureCanvas(self.figure)
        self.proxy_widget = self.scene.addWidget(self.canvas)
        # endregion
        # region 2nd window
        self.axes_2.clear()
        length_y = len(original_y)
        n_fft = 2048
        y_pad = util.fix_length(original_y, size=length_y + n_fft // 2)  # for saving the same signal after istft
        y_stft = stft(y_pad, n_fft=n_fft)
        amp_db = amplitude_to_db(abs(y_stft), ref=np.max)
        display.specshow(amp_db, cmap='Blues', y_axis='log', x_axis='time', ax=self.axes_2)
        self.axes_2.set_xlabel('Duration, s')
        self.axes_2.set_ylabel('Frequency, Hz')
        self.axes_2.set_title('Original signal in frequency domain, real part')
        self.canvas_2 = FigureCanvas(self.figure_2)
        self.proxy_widget = self.scene_2.addWidget(self.canvas_2)
        # endregion

    # todo: processed signal
    def processed_signal(self):
        """
        After a user have typed borders of a chosen frequency band,
        the current function removes the band
        and creates the bottom-right (frequency-time) and bottom-left (signal-time) plots,
        the bottom right displays frequencies without those were deleted,
        the bottom-left uses Inverse Short Time Fourier Transform and shows the result signal.
        :return:
        """
        try:                                   # get values of str type from line edits and checks them
            left = self.line_edit.text()
            right = self.line_edit_2.text()
            if not check_value(left, right):   # see check.py->check_value
                raise ValueError
        except ValueError:
            error_window()                     # see check.py->error_window
        else:
            # region 4th window
            self.axes_4.clear()
            orig_y, self.sr = load(self.name)
            n = len(orig_y)
            n_fft = 2048
            y_pad = util.fix_length(orig_y, size=n + n_fft // 2)  # for saving the same signal after istft
            y_stft = stft(y_pad, n_fft=n_fft)
            l = int(float(left) / 10)
            r = int(float(right) / 10)
            y_stft[[i for i in range(l, r)], :] = 0
            amp_db = amplitude_to_db(abs(y_stft), ref=np.max)
            display.specshow(amp_db, cmap='Blues', y_axis='log', x_axis='time', ax=self.axes_4)
            self.axes_4.set_xlabel('Duration, s')
            self.axes_4.set_ylabel('Frequency, Hz')
            self.axes_4.set_title('Processed signal in frequency domain, real part')
            self.canvas_4 = FigureCanvas(self.figure_4)
            self.proxy_widget = self.scene_4.addWidget(self.canvas_4)
            # endregion
            # region 3rd window
            self.last_y = istft(y_stft, length=n)
            self.axes_3.clear()
            display.waveshow(self.last_y, ax=self.axes_3)
            self.axes_3.grid(which='major')
            self.axes_3.minorticks_on()
            self.axes_3.grid(which='minor')
            self.axes_3.set_xlabel('Duration, s')
            self.axes_3.set_ylabel('Signal')
            self.axes_3.set_title('Processed signal in time domain')
            self.canvas_3 = FigureCanvas(self.figure_3)
            self.proxy_widget = self.scene_3.addWidget(self.canvas_3)
            # endregion

    # todo: save signal
    def save_signal(self):
        new_file, _ = QtWidgets.QFileDialog.getSaveFileName(filter='*.wav')
        if new_file:
            sf.write(new_file, self.last_y, self.sr)


# todo: main
# region launch
app = QtWidgets.QApplication(sys.argv)
win = UiMainWindow()
ui = Plot()
ui.show()
sys.exit(app.exec())
# endregion
