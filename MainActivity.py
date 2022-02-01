from pytube import YouTube
import PySimpleGUI as psg
import os

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
            self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xff


    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]


    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value


    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'


    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")


class TelaLayout:
    def __init__(self):
        layout = [
            [psg.Text('Link para download'), psg.Input(key='link')],
            [psg.FolderBrowse('Caminho'), psg.Input(key='path', default_text=get_download_folder())],
            [psg.Button('Baixar Audio', key='audio'), psg.Button('Baixar Video', key='video'), psg.Text('Resolução'),
             psg.Combo(values=["HD", "720p", "480p", "360p", "240p", "144p", "Menor"], key='resolution', size=(5, 1),
                       default_value='HD')]
        ]

        self.screen = psg.Window("Youtube Downloader By Vitaça", layout)

    def Start(self):
        while True:
            events, values = self.screen.read()
            if events == psg.WIN_CLOSED:
                break
            if events == "audio":
                link = values['link']
                path = values['path']

                youtube = YouTube(link)
                audio_ = youtube.streams.get_audio_only()
                try:
                    audio_.download(path)
                    psg.popup_ok('Download Concluido!')
                except:
                    psg.popup_ok('Falha no Download!')

            if events == "video":
                link = values['link']
                path = values['path']
                resolution = values['resolution']
                youtube = YouTube(link)
                if resolution == 'HD':
                    video_ = youtube.streams.get_highest_resolution()
                elif resolution == 'Menor':
                    video_ = youtube.streams.get_lowest_resolution()
                else:
                    video_ = youtube.streams.get_by_resolution(resolution=resolution)
                try:
                    video_.download(path)
                    psg.popup_ok('Download Concluido!')
                except:
                    psg.popup_ok('Falha no Download!')


screen = TelaLayout()
screen.Start()
