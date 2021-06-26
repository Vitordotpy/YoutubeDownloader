from pytube import YouTube
import PySimpleGUI as psg
import subprocess
import os


class TelaLayout:
    def __init__(self):
        layout = [
            [psg.Text('Link para download'), psg.Input(key='link')],
            [psg.FolderBrowse('Caminho'), psg.Input(key='path', default_text="C:\\users\\vitor\\downloads")],
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
