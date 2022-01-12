import ctypes
import threading
import time
from contextlib import redirect_stdout
from yt_dlp import YoutubeDL
import tkinter as tk
import platform

class TextOut(tk.Text):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

    def write(self, data):
        self.insert("insert", data)
        self.insert("insert", '\n')
        self.see("end")

    def flush(self):
        pass

class mainGui:
    def __init__(self):
        if platform.architecture()[1] == 'WindowsPE':
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.root = tk.Tk()
        self.root.title('youtubeDownloader')
        self.root.resizable(False, False)
        self.label1 = tk.Label(self.root, text="ProxyIP:")
        self.label2 = tk.Label(self.root, text="ProxyPort:")
        self.label3 = tk.Label(self.root, text="videoURL:")
        self.label4 = tk.Label(self.root, text="DownloadDir:")
        self.entry1 = tk.Entry(self.root)
        self.entry1.insert('end', '127.0.0.1:')
        self.entry2 = tk.Entry(self.root)
        self.entry2.insert('end', '10809')
        self.entry3 = tk.Entry(self.root, width=80)
        self.entry3.insert('end', 'https://www.youtube.com/watch?v=g6zKtbomjDc&ab_channel=ElizabethRabbit')
        self.entry4 = tk.Entry(self.root)
        self.entry4.insert('end', 'download/')
        self.button1 = tk.Button(self.root, text='start', command=self.btn1Cmd)
        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.label3.pack()
        self.entry3.pack()
        self.label4.pack()
        self.entry4.pack()
        self.button1.pack()
        self.logText = TextOut(self.root)
        self.logText.pack()
        self.root.mainloop()

        self.url = ''
        self.ip = ''
        self.port = ''
        self.downloadDir = ''

    def btn1Cmd(self):
        self.url = self.entry3.get()
        self.ip = self.entry1.get()
        self.port = self.entry2.get()
        self.downloadDir = self.entry4.get()
        if self.url:
            downloadProc = threading.Thread(target=self.dl, args=(self.ip, self.port, self.url, self.downloadDir))
            downloadProc.start()
        else:
            print(self.ip)
            print(self.port)
            print(self.url)

    def dl(self, proxyIP, proxyPort, dlURL, downloadDir):
        ydl_opts = {
            'proxy': proxyIP + proxyPort,
            'paths': {'home': downloadDir},
            'ffmpeg_location': 'ffmpegwin64/bin',
            'cookiefile': 'cookies-youtube-com.txt',
            'extractor_retries': 100,
            'external_downloader_args': ['-loglevel', 'panic'],
            'quiet': True,
            'no_warnings': True,
        }
        retryTimes = 1
        while retryTimes < 11:
            try:
                with redirect_stdout(self.logText):
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.download([dlURL])
                    print('done.')
                    break
            except Exception as exception:
                time.sleep(2)
                with redirect_stdout(self.logText):
                    print('download error, retry ' + str(retryTimes) + ' time.')
                    print(exception)
                    retryTimes = retryTimes + 1

if __name__ == '__main__':
    mainGui()