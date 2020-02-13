import sys, urllib, os, pathlib, subprocess
from Qtube_UI import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pytube import YouTube, helpers

def on_progress(stream, chunk, file_handle, bytes_remaining):
	filesize = stream.filesize
	win.Prog.filesize = filesize
	bytes_received = filesize - bytes_remaining
	win.Prog.bytes_received = bytes_received
	win.Prog._trigger_refresh()

def on_complete(stream, file_handle):
	if stream.is_progressive or stream.includes_audio_track or (not win.adapt):
		win.on_complete_signal.emit()
	win.Prog.bytes_received = 0

class Worker_1(QRunnable):
	@pyqtSlot()
	def run(self):
		win.on_begin_AV_signal.emit()
		win.vid_stream.download(output_path=win.fullpath.parent, filename='{}'.format(win.fullpath.stem))

class Worker_2(QRunnable):
	@pyqtSlot()
	def run(self):
		win.on_begin_V_signal.emit()
		win.vid_stream.download(output_path=win.fullpath.parent, filename='{}'.format(win.unique_path_video(win.fullpath.parent, win.fullpath.stem)))

		win.on_begin_A_signal.emit()
		win.aud_stream.download(output_path=win.fullpath.parent, filename='{}'.format(win.unique_path_audio(win.fullpath.parent, win.fullpath.stem)))

		subprocess.run(['ffmpeg', '-i', '{}'.format(win.video_path), '-i', '{}'.format(win.audio_path), '-codec', 'copy', '{}'.format(win.fullpath)])
		win.video_path.unlink()
		win.audio_path.unlink()
		win.adapt = False

class Worker_3(QRunnable):
	@pyqtSlot()
	def run(self):
		win.on_begin_A_signal.emit()
		win.aud_stream.download(output_path=win.fullpath.parent, filename='{}'.format(win.fullpath.stem))


class ProgressBar(QWidget):
	def __init__(self, *args, **kwargs):
		super(ProgressBar, self).__init__(*args, **kwargs)

	def paintEvent(self, e):
		if getattr(self, "bytes_received", None) is not None:
			painter = QPainter(self)

			brush = QBrush()
			brush.setColor(QColor('white'))
			brush.setStyle(Qt.SolidPattern)
			rect = QRect(0, 0, painter.device().width(), painter.device().height())
			painter.fillRect(rect, brush)

			padding = 2

			d_height = painter.device().height() - (padding * 2)
			d_width = painter.device().width() - (padding* 2)

			step_size = d_width / 15

			bar_width = step_size * 0.8
			bar_spacer = step_size * 0.1

			pc = self.bytes_received / self.filesize
			n_steps_to_draw = int(pc * 15)

			brush.setColor(QColor('green'))

			for n in range(n_steps_to_draw + 1):
				rect = QRect(
					padding + (n * step_size) + bar_spacer,
					padding,
					bar_width,
					d_height)
				painter.fillRect(rect, brush)

	def _trigger_refresh(self):
		self.repaint()

class MainWindow(QMainWindow, Ui_MainWindow):
	on_complete_signal = pyqtSignal()

	on_begin_AV_signal = pyqtSignal()
	on_begin_V_signal = pyqtSignal()
	on_begin_A_signal = pyqtSignal()

	def __init__(self, *args, **kwargs):
		super(QMainWindow, self).__init__(*args, **kwargs)
		
		self.setupUi(self)
		self.setWindowTitle('Qtube')

		self.threadpool = QThreadPool()

		self.StackedLayout1 = QStackedLayout(self.StackedMulti1)
		self.StackedLayout1.setObjectName('StackedLayout1')

		self.StackedLayout2 = QStackedLayout(self.StackedMulti2)
		self.StackedLayout2.setObjectName('StackedLayout2')

		self.EnterURL = QLineEdit()
		self.Prog = ProgressBar()
		self.StackedLayout1.addWidget(self.EnterURL)
		self.StackedLayout1.addWidget(self.Prog)

		self.DlButton1 = QPushButton('Download')
		self.StackedLayout2.addWidget(self.DlButton1)

		self.StreamSelectContainer = QWidget()
		self.StackedLayout2.addWidget(self.StreamSelectContainer)
		self.StreamSelectLayout = QVBoxLayout(self.StreamSelectContainer)

		self.SelectStream = QComboBox()
		self.DlButton2 = QPushButton('Download')

		self.StreamSelectLayout.addWidget(self.SelectStream)
		self.StreamSelectLayout.addWidget(self.DlButton2)

		self.DisplayStatus = QLabel()
		self.DisplayStatus.setFont(QFont('Arial', 20, QFont.Black))
		self.DisplayStatus.setAlignment(Qt.AlignCenter)

		self.StackedLayout2.addWidget(self.DisplayStatus)

		self.setFixedSize(375, 470)
		self.HighestQual.setCheckState(Qt.Checked)
		self.EnterURL.textChanged.connect(self.on_url_enter)
		self.DlButton1.pressed.connect(self.on_DL_pressed)
		self.DlButton2.pressed.connect(self.on_DL_pressed)
		self.StackedLayout2.setCurrentIndex(0)
		self.HighestQual.stateChanged.connect(self.on_hq_select)
		self.on_begin_AV_signal.connect(self.on_begin_AV_slot)
		self.on_begin_V_signal.connect(self.on_begin_V_slot)
		self.on_begin_A_signal.connect(self.on_begin_A_slot)		
		self.on_complete_signal.connect(self.on_complete_slot)

		self.can_dl = False
		self.adapt = False

	def populate_stream_select(self):
		for stream in self.vid.streams.all():
			if stream.is_progressive:
				self.SelectStream.addItem('Combined Video/Audio, {}, {}, {}'.format(stream.resolution, stream.abr, stream.mime_type))
			elif stream.includes_video_track:
				self.SelectStream.addItem('Video Only, {}, {}'.format(stream.resolution, stream.mime_type))
			elif stream.includes_audio_track:
				self.SelectStream.addItem('Audio Only, {}, {}'.format(stream.abr, stream.mime_type))

	def on_hq_select(self, s):
		if s == Qt.Checked:
			self.StackedLayout2.setCurrentIndex(0)
			self.AudioOnly.show()
		else:
			self.StackedLayout2.setCurrentIndex(1)
			self.AudioOnly.hide()

	def unique_path_audio(self, directory, name_pattern):
		counter = 0
		while True:
			self.audio_name = '{}_{}_{}'.format(name_pattern, 'audio', str(counter))
			self.audio_path = directory / '{}.{}'.format(self.audio_name, self.vid_stream.subtype)
			if not self.audio_path.exists():
				return self.audio_name
			counter += 1

	def unique_path_video(self, directory, name_pattern):
		counter = 0
		while True:
			self.video_name = '{}_{}_{}'.format(name_pattern, 'video', str(counter))
			self.video_path = directory / '{}.{}'.format(self.video_name, self.vid_stream.subtype)
			if not self.video_path.exists():
				return self.video_name
			counter += 1

	def on_url_enter(self, s):
		try:
			self.vid = YouTube(s, on_progress_callback = on_progress, on_complete_callback = on_complete)
						
			request = urllib.request.urlopen(self.vid.thumbnail_url).read()
			b4_resize = QPixmap()
			b4_resize.loadFromData(request)
			self.thumbnail = b4_resize.scaled(300, 350, Qt.KeepAspectRatio)
			self.ThumbnailView.setPixmap(self.thumbnail)

			self.populate_stream_select()

			self.can_dl = True

		except:
			self.ThumbnailView.setText('Please Enter a Valid Youtube Video URL')
			self.SelectStream.clear()
			self.can_dl = False

	def on_begin_AV_slot(self):
		self.StackedLayout1.setCurrentIndex(1)
		self.DisplayStatus.setText('Downloading Video/Audio')
		self.StackedLayout2.setCurrentIndex(2)

	def on_begin_A_slot(self):
		self.StackedLayout1.setCurrentIndex(1)
		self.DisplayStatus.setText('Downloading Audio')
		self.StackedLayout2.setCurrentIndex(2)

	def on_begin_V_slot(self):
		self.StackedLayout1.setCurrentIndex(1)
		self.DisplayStatus.setText('Downloading Video')
		self.StackedLayout2.setCurrentIndex(2)

	def on_complete_slot(self):
		self.StackedLayout1.setCurrentIndex(0)
		self.DisplayStatus.setText('')
		self.StackedLayout2.setCurrentIndex(0)

	def on_DL_pressed(self):
		if self.can_dl:
			if self.HighestQual.isChecked() and not self.AudioOnly.isChecked():
				self.vid_stream = self.vid.streams.filter(custom_filter_functions=[lambda s: s.includes_video_track]).order_by('resolution').desc().first()
				if self.vid_stream.is_progressive:
					fullpath, _ = QFileDialog.getSaveFileName(self, "Save file", helpers.safe_filename(self.vid.title), "{} (*.{});;All files (*.*)".format(self.suffix_description(self.vid_stream.subtype), self.vid_stream.subtype))
					if not fullpath:
						return
					self.fullpath = pathlib.Path(fullpath)

					worker = Worker_1()
					self.threadpool.start(worker)

				else:
					self.adapt = True

					self.aud_stream = self.vid.streams.filter(only_audio=True, subtype=self.vid_stream.subtype).first()
					
					fullpath, _ = QFileDialog.getSaveFileName(self, "Save file", helpers.safe_filename(self.vid.title), "{} (*.{});;All files (*.*)".format(self.suffix_description(self.aud_stream.subtype), self.aud_stream.subtype))
					if not fullpath:
						return
					self.fullpath = pathlib.Path(fullpath)

					worker = Worker_2()
					self.threadpool.start(worker)

			elif self.HighestQual.isChecked() and self.AudioOnly.isChecked():
				self.aud_stream = self.vid.streams.filter(only_audio=True).order_by('abr').desc().first()

				fullpath, _ = QFileDialog.getSaveFileName(self, "Save file", helpers.safe_filename(self.vid.title), "{} (*.{});;All files (*.*)".format(self.suffix_description(self.aud_stream.subtype), self.aud_stream.subtype))
				if not fullpath:
					return
				self.fullpath = pathlib.Path(fullpath)

				worker = Worker_3()
				self.threadpool.start(worker)

			else:
				print(self.SelectStream.currentIndex)
				
				self.vid_stream = self.vid.streams.all()[self.SelectStream.currentIndex()]

				fullpath, _ = QFileDialog.getSaveFileName(self, "Save file", helpers.safe_filename(self.vid.title), "{} (*.{});;All files (*.*)".format(self.suffix_description(self.vid_stream.subtype), self.vid_stream.subtype))
				if not fullpath:
					return
				self.fullpath = pathlib.Path(fullpath)

				worker = Worker_1()
				self.threadpool.start(worker)

	def suffix_description(self, suffix):
		if suffix == 'mp4':
			return 'MP4 File'
		return 'WebM File'
				

app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()
