#!/usr/bin/env python

#=======================================
# StoryBox
# Version: .1
# by Jessica Oros
#=======================================

import os, wx, threading
from subprocess import call, check_output

#-Settings-#
STORY_DIR = '../stories/'
STORY_FILENAME = 'story'
STORY_LENGTH = 60
VIDEO_HEIGHT = 900
VIDEO_WIDTH = 1400
VFLIP = False
HFLIP = False
DEBUG = False

RPANEL = 101
LPANEL = 102
PPANEL = 103
TEMP_DIR = 'rec/archive/'

class LoopPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY, size=(600,900))
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        clock = wx.StaticText(panel, wx.ID_ANY, ":" + str(STORY_LENGTH), style=wx.ALIGN_CENTER, size=(400,400))
        #blackout for now
        clock.SetForegroundColour('black')
        clock.SetBackgroundColour('black')
        clock.SetFont(wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record = wx.Button(panel2, wx.ID_ANY, label="Touch here to add your own story!", name='rpanel')
        record.SetForegroundColour('white')
        record.SetBackgroundColour('#28024f')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(clock, 0, flag=wx.ALIGN_RIGHT)
        vbox.Add(record, 1, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, flag=wx.EXPAND)
        sizer.Add(panel2, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)

class RecordPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY, size=(600,900))
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        clock = wx.StaticText(panel, wx.ID_ANY, ":" + str(STORY_LENGTH), style=wx.ALIGN_CENTER, size=(400,400))
        #blackout for now
        clock.SetForegroundColour('black')
        clock.SetBackgroundColour('#CCCCCC')
        clock.SetFont(wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record = wx.Button(panel2, wx.ID_ANY, label="Start Recording", name="lpanel")
        record.SetForegroundColour('white')
        record.SetBackgroundColour('#0072bb')
        record.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        record.Bind(wx.EVT_BUTTON, self.ToggleRecord)
        cancel = wx.Button(panel2, wx.ID_ANY, label="Cancel", name="lpanel")
        cancel.SetForegroundColour('white')
        cancel.SetBackgroundColour('#c5383e')
        cancel.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        cancel.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(record, 1, wx.EXPAND)
        hbox.Add(cancel, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(clock, 0, flag=wx.ALIGN_RIGHT)
        vbox.Add(hbox, 1, wx.EXPAND)
        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def ToggleRecord(self, e):
        global recording
        btn = e.GetEventObject()
        if not recording:
            wx.GetApp().StartRecording()
            btn.SetBackgroundColour('#932e72')
            btn.SetLabel('Stop Recording')
        else:
            wx.GetApp().StopRecording()
            btn.SetBackgroundColour('#0072bb')
            btn.SetLabel('Start Recording')
            self.GetParent().SwitchPanel(None, 'ppanel')

class PreviewPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour('black')
        panel = wx.Panel(self, wx.ID_ANY, size=(600,900))
        panel.SetBackgroundColour('black')
        panel2 = wx.Panel(self, wx.ID_ANY)
        panel2.SetBackgroundColour('black')
        clock = wx.StaticText(panel, wx.ID_ANY, ":" + str(STORY_LENGTH), style=wx.ALIGN_CENTER, size=(400,400))
        #blackout for now
        clock.SetForegroundColour('black')
        clock.SetBackgroundColour('#CCCCCC')
        clock.SetFont(wx.Font(100, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        save = wx.Button(panel2, wx.ID_ANY, label="Save", name="lpanel")
        redo = wx.Button(panel2, wx.ID_ANY, label="Redo", name="rpanel")
        cancel = wx.Button(panel2, wx.ID_ANY, label="Cancel", name="lpanel")
        cancel.SetForegroundColour('white')
        cancel.SetBackgroundColour('#c5383e')
        cancel.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        cancel.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        save.SetForegroundColour('white')
        save.SetBackgroundColour('green')
        save.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        save.Bind(wx.EVT_BUTTON, wx.GetApp().SaveVideo)
        redo.SetForegroundColour('white')
        redo.SetBackgroundColour('#0072bb')
        redo.SetFont(wx.Font(36, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        redo.Bind(wx.EVT_BUTTON, parent.SwitchPanel)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(save, 1, wx.EXPAND)
        hbox.Add(redo, 1, wx.EXPAND)
        hbox.Add(cancel, 1, wx.EXPAND)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(clock, 0, wx.ALIGN_RIGHT)
        vbox.Add(hbox, 1, wx.EXPAND)

        panel.SetSizer(vbox)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        sizer.Add(panel2, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
class SBFrame(wx.Frame):

    def __init__(self, parent, title):

        global storybox;
        storybox = wx.GetApp()

        #setup panels
        wx.Frame.__init__(self, None, wx.ID_ANY, "Storybox")
        self.lpanel = LoopPanel(self)
        self.rpanel = RecordPanel(self)
        self.ppanel = PreviewPanel(self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.lpanel, 1, wx.EXPAND)
        self.sizer.Add(self.rpanel, 1, wx.EXPAND)
        self.sizer.Add(self.ppanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

        #setup menus
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        switch_to_rpanel = fileMenu.Append(RPANEL, "Switch to &Record Panel")
        switch_to_ppanel = fileMenu.Append(PPANEL, "Switch to &Preview Panel")
        switch_to_lpanel = fileMenu.Append(LPANEL, "Switch to &Loop Panel")
        cleanup = fileMenu.Append(wx.ID_ANY, "Cleanup (kill processes)")
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_rpanel)
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_lpanel)
        self.Bind(wx.EVT_MENU, self.SwitchPanel, switch_to_ppanel)
        self.Bind(wx.EVT_MENU, storybox.CleanUp, cleanup)
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    def HidePanels(self):
        self.lpanel.Hide()
        self.ppanel.Hide()
        self.rpanel.Hide()
        
    def SwitchPanel(self, e=None, panel=""):
        self.HidePanels()

        if not panel:
            #switching from menu
            panel = e.GetId()
            if panel is RPANEL:
                panel = 'rpanel'
            elif panel is LPANEL:
                panel = 'lpanel'
            elif panel is PPANEL:
                panel = 'ppanel'
            else:
                #switching from button
                btn = e.GetEventObject()
                panel = btn.GetName()

        if panel == 'rpanel':
            wx.GetApp().RecordPanel()
        if panel == 'lpanel':
            wx.GetApp().LoopPanel()
        if panel == 'ppanel':
            wx.GetApp().PreviewPanel()

        self.Layout()

class StoryBox(wx.App):
    def OnInit(self):
        self.frame = SBFrame(None, "Storybox")
        self.SetTopWindow(self.frame)
        self.frame.Maximize()
        if not DEBUG:
            self.frame.ShowFullScreen(True)
        else:
            self.frame.Show(True)

        #init LoopPanel
        self.frame.HidePanels()
        self.LoopPanel()

        global encoding
        encoding = 0

        return True;

    def LoopVideos(self):
        global looping
        looping = True
        while looping:
            files = os.listdir(STORY_DIR)
            for file in files:
                call(['omxplayer','--win','200 0 1700 900', STORY_DIR + file])
                #call(['omxplayer','--win','0 0 100 100', STORY_DIR + file])
                if not looping:
                    break

    def PreviewCamera(self):
        #call(['picam', '--alsadev', 'hw:1,0', '--previewrect', '0,0,100,100'])
        call(['picam', '--alsadev', 'hw:1,0', '--previewrect', '200,0,1400,900'])

    def StartRecording(self):
        global recording
        open('hooks/start_record', 'w')
        recording = True

    def StopRecording(self):
        global recording
        open('hooks/stop_record', 'w')
        recording = False
        self.frame.SwitchPanel(None, 'ppanel')

    def PreviewVideo(self):
        global previewing
        previewing = True
        while previewing:
            #call('omxplayer --win "0 0 100 100" rec/archive/*.ts', shell=True)
            call('omxplayer --win "200 0 1700 900" rec/archive/*.ts', shell=True)
            if not previewing:
                break

    def SaveVideo(self, e):
        global encoding
        ffmpeg = threading.Thread(target=self.EncodeVideo)
        ffmpeg.start()
        ffmpeg.join()
        self.frame.SwitchPanel(e)

    def EncodeVideo(self):
        global encoding
        encoding += 1
        files = os.listdir(STORY_DIR)
        new_story = STORY_DIR + STORY_FILENAME + str(len(files)+1) + '.mp4'
        call('ffmpeg -i ' + TEMP_DIR + '*.ts -c:v copy -c:a copy -bsf:a aac_adtstoasc ' + new_story, shell=True)
        encoding -= 1
        
    def LoopPanel(self):
        self.CleanUp()
        self.DeleteTempFiles()
        self.frame.lpanel.Show()
        #start video loop
        loop = threading.Thread(target=self.LoopVideos)
        loop.start()

    def RecordPanel(self):
        self.CleanUp()
        self.DeleteTempFiles()
        self.frame.rpanel.Show()
        #start camera
        camera = threading.Thread(target=self.PreviewCamera)
        camera.start()
            
    def PreviewPanel(self):
        self.CleanUp()
        self.frame.ppanel.Show()
        #preview video
        preview = threading.Thread(target=self.PreviewVideo)
        preview.start()

    def CleanUp(self, e=None):
        global looping, recording, previewing
        previewing = False
        looping = False
        recording = False
        pkill = call('pkill omxplayer', shell=True)
        pkill = call('pkill picam', shell=True)

    def DeleteTempFiles(self):
        call('rm -rf hooks state rec', shell=True)
    
if __name__ == '__main__':
    sb = StoryBox()
    sb.MainLoop()
