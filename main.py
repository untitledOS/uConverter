import sys, yt_dlp, toml
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from config_tools import get_config

class DownloadThread(QThread):
    progress_signal = Signal(int)

    def __init__(self, url, av_format, parent=None):
        super().__init__(parent)
        self.url = url
        self.format = av_format

    def run(self):
        audio_formats = ["mp3", "wav", "flac", "vorbis", "m4a", "aac", "opus"]
        if self.format in audio_formats:
            self.download_audio()
        else:
            self.download_video()

    def my_hook(self, d):
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            self.progress_signal.emit(p)

    def download_audio(self):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.format,
            }],
            'ffmpeg_location': 'ffmpeg.exe',
            'progress_hooks': [self.my_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def download_video(self):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.format,
            }],
            'ffmpeg_location': 'ffmpeg.exe',
            'progress_hooks': [self.my_hook],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

class SettingsWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
        self.layout = QtWidgets.QVBoxLayout(self)
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())

        self.text = QtWidgets.QLabel("Settings", alignment=QtCore.Qt.AlignTop)
        self.text.setStyleSheet("font-size: 24px; font-weight: normal;")
        self.layout.addWidget(self.text)

        self.download_path_label = QtWidgets.QLabel("Downloads Folder", alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.download_path_label)

        self.download_path = QtWidgets.QLineEdit(self)
        self.download_path.setPlaceholderText("Download Path")
        self.download_path.setText(get_config()["Settings"]["download_path"])
        self.layout.addWidget(self.download_path)

        self.download_path_button = QtWidgets.QPushButton("Browse")
        self.download_path_button.setObjectName("minor")
        self.download_path_button.clicked.connect(self.browse)
        self.layout.addWidget(self.download_path_button)

        self.layout.addStretch()

        self.button = QtWidgets.QPushButton("Apply")
        self.button.clicked.connect(self.apply_settings)
        self.layout.addWidget(self.button)

    def apply_settings(self):
        config = get_config()
        config["Settings"]["download_path"] = self.download_path.text()
        with open("config.toml", "w") as f:
            toml.dump(config, f)
        self.close()

    def browse(self):
        self.download_path.setText(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.settings_window = SettingsWindow()
        self.setWindowTitle("Trapeze")
        self.layout = QtWidgets.QVBoxLayout(self)
        with open("style.css", "r") as f:
            self.setStyleSheet(f.read())

        self.settings_button = QtWidgets.QPushButton("Settings")
        self.settings_button.setIcon(QtGui.QIcon("icons/settings.svg"))
        self.settings_button.setObjectName("settings_button")
        self.settings_button.clicked.connect(self.settings_window.show)
        self.layout.addWidget(self.settings_button)

        self.tabs = QtWidgets.QTabWidget()
        self.conversion_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.conversion_tab, "Conversion")
        self.youtube_download_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.youtube_download_tab, "YouTube Download")
        self.about_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.about_tab, "About")
        self.tabs.setCurrentIndex(1)
        self.layout.addWidget(self.tabs)

        self.conversion_tab_layout = QtWidgets.QVBoxLayout(self.conversion_tab)

        self.text = QtWidgets.QLabel("Conversion", alignment=QtCore.Qt.AlignTop)
        self.conversion_tab_layout.addWidget(self.text)

        self.file_input_layout = QtWidgets.QHBoxLayout()
        self.conversion_tab_layout.addLayout(self.file_input_layout)

        self.file_input = QtWidgets.QLineEdit(self)
        self.file_input.setPlaceholderText("Select a file...")
        self.file_input_layout.addWidget(self.file_input)

        self.file_input_button = QtWidgets.QPushButton("Browse")
        self.file_input_button.setObjectName("minor")
        self.file_input_button.clicked.connect(self.browse_conversion)
        self.file_input_layout.addWidget(self.file_input_button)

        self.format_layout = QtWidgets.QHBoxLayout()
        self.conversion_tab_layout.addLayout(self.format_layout)

        self.format_label = QtWidgets.QLabel("Convert to:", alignment=QtCore.Qt.AlignTop)
        self.format_layout.addWidget(self.format_label)

        self.format_selection = QtWidgets.QComboBox(self)
        self.format_selection.addItems(["MPEG 4 (MP4)", "Matroska (MKV)", "Web Media Video (WEBM)", "Audio Video Interleave (AVI)", "MPEG 3 (MP3)", "Waveform (WAV)", "Free Lossless Audio Codec (FLAC)", "OGG", "iTunes Media (M4A)", "Advanced Audio Coding (AAC)", "Opus"])
        self.format_dict = {"MPEG 4 (MP4)": "mp4", "Matroska (MKV)": "mkv", "Web Media Video (WEBM)": "webm", "Audio Video Interleave (AVI)": "avi", "MPEG 3 (MP3)": "mp3", "Waveform (WAV)": "wav", "Free Lossless Audio Codec (FLAC)": "flac", "OGG": "vorbis", "iTunes Media (M4A)": "m4a", "Advanced Audio Coding (AAC)": "aac", "Opus": "opus"}
        self.format_layout.addWidget(self.format_selection)

        self.conversion_tab_layout.addStretch()

        self.convert_button = QtWidgets.QPushButton("Convert")
        self.conversion_tab_layout.addWidget(self.convert_button)

        self.youtube_download_tab_layout = QtWidgets.QVBoxLayout(self.youtube_download_tab)

        self.text = QtWidgets.QLabel("YouTube Download", alignment=QtCore.Qt.AlignTop)
        self.youtube_download_tab_layout.addWidget(self.text)
        
        # User Input
        self.url_input_box = QtWidgets.QLineEdit(self)
        self.url_input_box.setPlaceholderText("Enter a URL...")
        self.url_input_box.setText("https://www.youtube.com/watch?v=Wba8tHRY3Ic")
        self.url_input_box.setStyleSheet("border: 2px solid grey; border-radius: 12px; padding: 5px;")
        # self.url_input_box.textChanged.connect(self.get_quality_options)
        self.youtube_download_tab_layout.addWidget(self.url_input_box)

        # # Quality Selection
        # self.quality_label = QtWidgets.QLabel("Video Quality", alignment=QtCore.Qt.AlignTop)
        # self.layout.addWidget(self.quality_label)
        # self.quality_selection = QtWidgets.QComboBox(self)
        # self.quality_selection.addItems(["Select a valid URL"])
        # self.quality_selection.setDisabled(True)
        # self.layout.addWidget(self.quality_selection)

        self.av_format = QtWidgets.QComboBox(self)
        self.av_format.addItems(["MPEG 4 (MP4)", "Matroska (MKV)", "Web Media Video (WEBM)", "Audio Video Interleave (AVI)", "MPEG 3 (MP3)", "Waveform (WAV)", "Free Lossless Audio Codec (FLAC)", "OGG", "iTunes Media (M4A)", "Advanced Audio Coding (AAC)", "Opus"])
        self.format_dict = {"MPEG 4 (MP4)": "mp4", "Matroska (MKV)": "mkv", "Web Media Video (WEBM)": "webm", "Audio Video Interleave (AVI)": "avi", "MPEG 3 (MP3)": "mp3", "Waveform (WAV)": "wav", "Free Lossless Audio Codec (FLAC)": "flac", "OGG": "vorbis", "iTunes Media (M4A)": "m4a", "Advanced Audio Coding (AAC)": "aac", "Opus": "opus"}
        self.youtube_download_tab_layout.addWidget(self.av_format)

        self.sponsor_block = QtWidgets.QCheckBox("Remove Video Sponsors")
        self.sponsor_block.setChecked(get_config()["Settings"]["sponsor_block"])
        self.youtube_download_tab_layout.addWidget(self.sponsor_block)

        self.youtube_download_tab_layout.addStretch()

        self.button = QtWidgets.QPushButton("Download")
        self.button.setObjectName("youtube_red")
        self.youtube_download_tab_layout.addWidget(self.button)

        # self.progress_bar = QtWidgets.QProgressBar(self)
        # self.progress_bar.setValue(0)
        # self.layout.addWidget(self.progress_bar)

        self.button.clicked.connect(self.yt_download)

        self.about_tab_layout = QtWidgets.QVBoxLayout(self.about_tab)

        self.about_title = QtWidgets.QLabel("About", alignment=QtCore.Qt.AlignTop)
        self.about_tab_layout.addWidget(self.about_title)

        self.about_text = QtWidgets.QLabel("Trapeze is an Audio and Video Megatool. It's like the Swiss Army Knife of media conversion and downloading. It's built with Python and Qt, and uses yt-dlp for downloading videos and audio from YouTube.\n\nLicense: MIT\n\nAuthor: Ethan Martin")
        self.about_text.setStyleSheet("font-weight: normal;")
        self.about_text.setWordWrap(True)
        self.about_text.setOpenExternalLinks(True)
        self.about_tab_layout.addWidget(self.about_text)
        
        self.about_tab_layout.addStretch()

    def browse_conversion(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Select a file...", "", "Video & Audio Files (*.mp4 *.mkv *.webm *.avi *.mp3 *.wav *.flac *.ogg *.m4a *.aac *.opus)")
        self.file_input.setText(file_name[0])

    @QtCore.Slot(int)
    def update_progress(self, progress):
        # self.progress_bar.setValue(progress)
        pass

    @QtCore.Slot()
    def yt_download(self):
        for element in self.children():
            try:
                element.setDisabled(True)
            except AttributeError:
                pass
        self.button.setText("Downloading...")

        self.download_thread = DownloadThread(url=self.url_input_box.text(), av_format=self.format_dict[self.av_format.currentText()])
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    @QtCore.Slot()
    def on_download_finished(self):
        for element in self.children():
            try:
                element.setDisabled(False)
            except AttributeError:
                pass
        self.button.setText("Download")

    def get_quality_options(self):
        try:
            # get quality options using yt-dlp
            ydl = yt_dlp.YoutubeDL({'quiet': True})
            with ydl:
                result = ydl.extract_info(self.url_input_box.text(), download=False)
                if 'entries' in result:
                    # Can be a playlist or a list of videos
                    video = result['entries'][0]
                else:
                    # Just a video
                    video = result
                self.quality_selection.clear()
                self.quality_selection.addItems([result])
                self.quality_selection.setDisabled(False)
        except Exception as e:
            self.quality_selection.clear()
            self.quality_selection.addItems([e])
            self.quality_selection.setDisabled(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.setFixedWidth(450)
    widget.setFixedHeight(350)
    widget.show()

    sys.exit(app.exec())
